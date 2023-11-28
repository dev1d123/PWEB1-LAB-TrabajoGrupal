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
#my $new_title = $cgi->param'nuevo_titulo';
#my $new_textMarkdown = '###prueba y error';

my $consulta = "UPDATE files SET file_name = 'cocumento coco', file_content = 'Hola a todos, soy vegetta 777' WHERE id = $id";

# Ejecutar la consulta
my $sth = $dbh->prepare($consulta);
$sth->execute() or die "Error al ejecutar la consulta: $DBI::errstr";

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

print $cgi->header('text/html');
print "La pagina a sido actualizada <br>\n";

print "<td><form action='lista.cgi' method='post'>";
print "<input type='submit' value='Continuar'>";
print "</form></td>";

# Desconectar
$dbh->disconnect;