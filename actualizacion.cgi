#!"C:/xampp/perl/bin/perl.exe"
use CGI ':standard';
use utf8;
use CGI::Carp qw(fatalsToBrowser);
use DBI;

#markdown -> html
my $cgi = CGI -> new;
my $title = $cgi->param('title');
my $textMarkdown = $cgi->param('markdown');

#Variables de conexion:
my $database = 'markdown';
my $hostname = '127.0.0.1';
my $port = 3306;
my $user = 'root';
my $password = 'root';

#Creacion del texto Markdown

print $cgi->header('text/html');
print '<link rel="stylesheet" type="text/css" href="estilos/estilos-cgi.css">' . "\n";
print "La pagina ha sido creada <br>\n";

# String de conexión
my $dsn = "DBI:mysql:database=$database;host=$hostname;port=$port";


# Conectar
my $dbh = DBI->connect($dsn, $user, $password, { RaiseError => 1 }) 
    or die $DBI::errstr;

# Realizar operaciones aquí...

# Preparar la sentencia SQL
my $sth = $dbh->prepare("INSERT INTO files (file_name, file_content) VALUES (?, ?)");

# Ejecutar la sentencia
$sth->execute($title, $textMarkdown)
    or die "No se pudo ejecutar la consulta: $sth->errstr";

print "<td><form action='lista.cgi' method='post'>";
print "<input type='submit' value='Continuar'>";
print "</form></td>";

# Desconectar
$dbh->disconnect;

print "</body></html>\n";