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

# Desconectar
$dbh->disconnect;