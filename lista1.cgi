#!"C:/xampp/perl/bin/perl.exe"
use CGI ':standard';
use utf8;
use CGI::Carp qw(fatalsToBrowser);
use DBI;

print "Content-type: text/html\n\n";
print "<html><head><title>Resultados</title></head><body>\n";
print "<h1>Resultados de la Consulta</h1>\n";

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
my $nombre_archivo = "$title.txt";
open my $archivo, '>', "baseDatos/$nombre_archivo";
my @lines = split /\n/, $textMarkdown; 
foreach my $line (@lines) {
    print $archivo "$line\n";
}
close $archivo;

#Creacion del texto Markdown

print $cgi->header('text/html');
print "El titulo es $title <br>\n";

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
    
my $pth = $dbh->prepare("SELECT id, file_name, file_content FROM files");

$pth->execute()
    or die "No se pudo ejecutar la consulta: $sth->errstr";

    print "<table border='1'>\n";
    print "<tr><th>Nombres</th></tr>\n";
   
    while (my @row = $pth->fetchrow_array) {  
    print "<tr><td>$row[1]</td>";

    print "<td><form action='convert.cgi' method='get'>";
    print "<input type='hidden' name='id' value='$row[0]'>";
    print "<input type='submit' value='V'>";
    print "</form></td>";

    print "<td><form action='convert.cgi' method='get'>";
    print "<input type='hidden' name='id' value='$row[0]'>";
    print "<input type='submit' value='E'>";
    print "</form></td>";

    print "<td><form action='convert.cgi' method='get'>";
    print "<input type='hidden' name='id' value='$row[0]'>";
    print "<input type='submit' value='X'>";
    print "</form></td>\n";
}

print "</table>\n";

# Desconectar
$dbh->disconnect;

print "</body></html>\n";