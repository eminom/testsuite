
use 5.012;
use strict;
use warnings;
use Digest::MD5 qw/md5 md5_hex/;
use Digest::xxHash qw[xxhash32 xxhash32_hex];
use Cwd qw/getcwd/;

my $host = "localhost";
my $port = 13000;

sub hashXX {
   my $full = shift // die 'no input file specified';
   my $seed = "10241024";  # Good seed.
   open my $fin, '<', $full or die "Cannot open $full\n";
   binmode($fin);
   read($fin, my $data, -s $full);
   close $fin;
   xxhash32_hex($data, $seed);
}

sub uploadFile {
    my $presub = shift // die;
    my $full = shift // die;
    my $xxhashR = hashXX $full;
    my $uri = "http://$host:$port/upload.jsp?name=$presub&hash=$xxhashR";
    my $cmd = "curl -i -T \"$full\" \"$uri\"";
    #print $cmd,"\n";
    #system($cmd);
    `$cmd`;
    die "upload for $uri failed" if $?;
    #my $pid = fork;
    #die "Fork error" if !defined($pid);
    #if(0==$pid){
    #    system($cmd);
    #    exit;
    #}
}

sub processorTask {
    my $arr = shift // die "NO NO";
    for my $ent(@{$arr}){
        #my ($sub, $full) = @{$ent};
        #print "$sub\n";
        uploadFile @{$ent};
    }
}

# Parameters
# 
sub walkNow {
    my $baseNow = shift // die "no base";   # $baseNow shall always ends with a slash. 
    my $dirNow  = shift // die "no dir for now";
    my $refArr  = shift // die "no ref array for now";
    # my $pro_ref = shift // \&dummm;
    my @nextD;
    opendir my $cd, $dirNow or die "no open for \"$dirNow\"";
    while (my $f = readdir $cd)  {
        next if grep{$f eq $_} qw/. .. .git .gitignore/;
        my $now = $dirNow . '/'. $f;
        if(-d $now) {
            push @nextD, $now;
            next;
        }
        # Filter some files out
        # if( $f !~ /\.pl$/imxs &&
        #     $f !~ /\.pm$/imxs) {
        #     #print $now,"\n";
        #     # $pro_ref->($sub, $now);
        # }
        my $sub = substr($now, length($baseNow));
        push @{$refArr}, [$sub, $now];
        #uploadFile $sub, $now;
    }
    closedir $cd;
    walkNow($baseNow, $_, $refArr) for @nextD;
}

if (!@ARGV) {
    #print "Need target ip\n";
    #exit -1;
    $host = "localhost";
} else {
    $host = $ARGV[0];
    $host = "localhost" if $host !~ /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/i;
}

my $start = getcwd;    #Ends without slash
die "not a source directory for $start" if not -d $start;
my @arr;
walkNow $start.'/', $start, \@arr;

#print scalar @arr, "\n";
#print $#arr,"\n";
#print "*"x20, "\n";

my $count = scalar @arr;
my $row = 1;
my $col = int($count / $row);
++$row if $count % $row;
my @pids;
while (@arr) {
    my @jobs = splice @arr, 0, $col;
    my $pid = fork;
    if (0==$pid) {
        processorTask(\@jobs);
        exit;
    } else {
        push @pids, $pid;
    }
}
#print "${$_}[0]\n${$_}[1]\n" for @arr;
waitpid $_, 0 for @pids;
print "done\n";
