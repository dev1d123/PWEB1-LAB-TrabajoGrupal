#!"C:/xampp/perl/bin/perl.exe"
use CGI ':standard';
use utf8;
use CGI::Carp qw(fatalsToBrowser);
use DBI;

#Variables de conexion:
my $database = 'markdown';
my $hostname = '127.0.0.1';
my $port = 3306;
my $user = 'root';
my $password = 'root';

#Creacion del texto Markdown
my $nombre_archivo = "$title.txt";
open my $archivo, '>', "baseDatos/$nombre_archivo";
my @lines = split /\n/, $textMarkdown; 
foreach my $line (@lines) {
    print $archivo "$line\n";
}
close $archivo;

# String de conexión
my $dsn = "DBI:mysql:database=$database;host=$hostname;port=$port";

# Conectar
my $dbh = DBI->connect($dsn, $user, $password, { RaiseError => 1 }) 
    or die $DBI::errstr;

my $cgi = CGI -> new;
my $id = $cgi->param('id');


my $sth = $dbh->prepare("SELECT id, file_name, file_content FROM files WHERE id = $id");

$sth->execute()
    or die "No se pudo ejecutar la consulta: $sth->errstr";

#markdown -> html
my $title;
my $textMarkdown;

while (my @row = $sth->fetchrow_array) {
    $title = $row[1];
    $textMarkdown = $row[2]
}


#Creacion del texto Markdown
my $nombre_archivo = "$title.txt";
open my $archivo, '>', "baseDatos/$nombre_archivo";
my @lines = split /\n/, $textMarkdown; 
foreach my $line (@lines) {
    print $archivo "$line\n";
}
close $archivo;

print $cgi->header('text/html');
print "El titulo es $title <br>\n";
print "El ID es: $id <br>\n";

my $k = 0;

while ($k < scalar(@lines)) {
    my $line = $lines[$k];

    if (substr($line, 0, 3) eq "```") {
        my $initialIndex = $k + 1;
        my $finalIndex = scalar(@lines);

        for (my $i = $initialIndex; $i < scalar(@lines); $i++) {
            if (substr($lines[$i], 0, 3) eq "```") {
                $finalIndex = $i;
                last;
            }
        }

        my $ans = "";
        for (my $i = $initialIndex; $i < $finalIndex; $i++) {
            $ans .= "$lines[$i]<br>";
        }

        $ans = "<p><code>$ans</code></p>";
        print "$ans";

        $k = $finalIndex + 1; 
    } else {
        my $wow = procesar_formato($line);
        print "$wow";
        $k++;
    }
}

#Primero, encontrar el tag
sub procesar_formato(){
    my ($line) = @_;
    my $ans = $line;

    #Primero procesamos los headers.
    if(substr($line, $i, 6) eq "######"){
        $line = substr($line, 6, length($line));
        $ans = "<h6>$line</h6>";
        return $ans;
    }elsif(substr($line, $i, 5) eq "#####"){
        $line = substr($line, 5, length($line));
        $ans = "<h5>$line</h5>";
                return $ans;

    }elsif(substr($line, $i, 4) eq "####"){
        $line = substr($line, 4,length($line));
        $ans = "<h4>$line</h4>";
                return $ans;

    }elsif(substr($line, $i, 3) eq "###"){
        $line = substr($line, 3, length($line));
        $ans = "<h3>$line</h3>";
                return $ans;

    }elsif(substr($line, $i, 2) eq "##"){
        $line = substr($line, 2, length($line));
        $ans = "<h2>$line</h2>";
                return $ans;

    }elsif(substr($line, $i, 1) eq '#'){
        $line = substr($line, 1, length($line));
        $ans = "<h1>$line</h1>";
                return $ans;
    }


    for (my $i = 0; $i < length($line); $i++) {
        if(substr($line, $i, 3) eq "***"){
            my $initialIndex = $i + 3;
            my $finalIndex;

            for(my $j = $i + 1; $j < length($line) - 2; $j++){
                if(substr($line, $j, 3) eq "***"){
                    $finalIndex = $j;
                    last;
                }
            }
            my $wrappedText = substr($line, $initialIndex, $finalIndex - $initialIndex);
            $line = substr($line, 0, $i) . "<strong><em>$wrappedText</em></strong>" . substr($line, $finalIndex + 3);
        }elsif(substr($line, $i, 2) eq "**"){
            my $initialIndex = $i + 2;
            my $finalIndex;

            for (my $j = $i + 1; $j < length($line) - 1; $j++) {
                if (substr($line, $j, 2) eq "**") {
                    $finalIndex = $j;
                    last;
                }
            }
            my $wrappedText = substr($line, $initialIndex, $finalIndex - $initialIndex);
            $line = substr($line, 0, $i) . "<strong>$wrappedText</strong>" . substr($line, $finalIndex + 2);
        }elsif(substr($line, $i, 1) eq '*' || substr($line, $i, 1) eq "_"){
            my $initialIndex = $i + 1;
            my $finalIndex;
            for (my $j = $i + 1; $j < length($line); $j++) {
                if (substr($line, $j, 1) eq "*" || substr($line, $j, 1) eq "_") {
                    $finalIndex = $j;
                    last;
                }
            }
            my $wrappedText = substr($line, $initialIndex, $finalIndex - $initialIndex);
            $line = substr($line, 0, $i) . "<em>$wrappedText</em>" . substr($line, $finalIndex + 1);
        }
            if(substr($line, $i, 2) eq "~~"){
                my $initialIndex = $i + 2;
                my $finalIndex;

                for (my $j = $i + 1; $j < length($line) - 1; $j++) {
                    if (substr($line, $j, 2) eq "~~") {
                        $finalIndex = $j;
                        last;
                    }
                }
                my $wrappedText = substr($line, $initialIndex, $finalIndex - $initialIndex);
                $line = substr($line, 0, $i) . "<del>$wrappedText</del>" . substr($line, $finalIndex + 2);
            }
            #para los enlaces 
        if (substr($line, $i, 1) eq '[') {
            my $texto;
            if ($line =~ /([^\[\(]+)(?=\[|\()/) {
                $texto = $1;
            }
            my $textoEnlace;
            if ($line =~ /\[(.*?)\]/) {
                $textoEnlace = $1;
            }
            my $direccion;
            if ($line =~ /\((.*?)\)/) {
                $direccion = $1;
            }

            return "<p>$texto<a href = '$direccion'>$textoEnlace</a></p>";
        }

    }
    $ans = "<p>$line</p>";
    return $ans;
}

# Desconectar
$dbh->disconnect;