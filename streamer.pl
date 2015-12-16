
use 5.012;
use strict;
use warnings;
use Cwd qw/getcwd/;

my $host = "localhost";
my $port = 13000;

sub uploadFile {
    my $presub = shift // die;
    my $full = shift // die;
    my $uri = "http://$host:$port/upload.jsp?name=$presub";
    my $cmd = "curl -i -T \"$full\" $uri";
    print $cmd,"\n";
    my $pid = fork;
    die "Fork error" if !defined($pid);
    if(0==$pid){
        system($cmd);
        exit;
    }
}

# Parameters
# 
sub walkNow{
    my $baseNow = shift // die "no base";   # $baseNow shall always ends with a slash. 
    my $dirNow  = shift // die "no dir for now";
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
        uploadFile $sub, $now;
    }
    closedir $cd;
    walkNow($baseNow, $_) for @nextD;
}

my $start = getcwd;
die "not a source directory for $start" if not -d $start;
walkNow($start.'/', $start);
waitpid -1, 0;
