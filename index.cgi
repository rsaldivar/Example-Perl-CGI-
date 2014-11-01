#!/usr/bin/perl

require ("header.cgi"); #add header

print '<script type="text/javascript"> 
$(document).ready(function(){
    $("#myModalCompra").modal("show");
});
</script>';

my $query = new CGI;
my(%VariablesGet); #Iniciamos el hash
my $bufferGet = $ENV{'QUERY_STRING'};
my @pairs = split(/&/, $bufferGet);
foreach my $pair (@pairs) {
my ($nameGet, $valueGet) = split(/=/, $pair);
$nameGet =~ tr/+/ /;
$nameGet =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
$valueGet =~ tr/+/ /;
$valueGet =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
$VariablesGet{$nameGet} = $valueGet;
}
#=============================================== RECOGER GET


my @ArrayEntrada = $query->param;
my %GetHash;
foreach my $atributo (@ArrayEntrada)
{	$GetHash{$atributo} = $query->param($atributo);
}
#=============================================== RECOGER POST



my $dbh = DBI->connect("dbi:mysql:themach2_ticketmaster", 'themach2_usuario', 'optiplex') or die "Error de conexion: \n";





my $seccion = $GetHash{'seccion'};
my $cliente = $GetHash{'cliente'};
use POSIX qw/ strftime /;
my $magico = strftime( "%d%m%H%M%S", localtime(time) );
my $precio = $GetHash{'precio'};
my $cantidad = $GetHash{'cantidad'};
if($VariablesGet{'comprado'}  eq "true")
{
  my $sqlAlta = 'insert into boleto ( id, tipoBoleto_id, seccion_nombre ) values ( '.$magico.' , 1, "'.$seccion.'" )'; 
  my $sthAlta = $dbh->prepare( $sqlAlta );## Preparar la sentencia de insercion en la base de datos
     $sthAlta->execute();
  my $sqlAlta = 'insert into compra ( id, total , cliente_id ) values ( '.$magico.' , '.$precio*$cantidad.' , "'.$cliente.'" )'; 
  my $sthAlta = $dbh->prepare( $sqlAlta );## Preparar la sentencia de insercion en la base de datos
     $sthAlta->execute();
 my $sqlAlta = 'insert into compra_has_boleto (compra_id , boleto_id ) values( '.$magico.' ,'.$magico.' ) ';
  my $sthAlta = $dbh->prepare( $sqlAlta );## Preparar la sentencia de insercion en la base de datos
     $sthAlta->execute();
 
}

if($VariablesGet{'compra'}  eq "true")
{
    $evento = $VariablesGet{'evento'};  
    my $sqlConsulta = 'SELECT evento.nombre, evento.fecha, evento.hora, ciudad.nombre, foro.nombre FROM categoria INNER JOIN subcategoria ON 
subcategoria.categoria_nombre = categoria.nombre INNER JOIN evento ON evento.subcategoria_nombre = subcategoria.nombre INNER JOIN evento_has_foro ON 
evento_has_foro.evento_nombre = evento.nombre INNER JOIN foro ON foro.nombre = evento_has_foro.foro_nombre INNER JOIN ciudad ON ciudad.id = 
foro.ciudad_id INNER JOIN estado ON estado.id = ciudad.estado_id  WHERE evento.nombre = "'.$evento.'" ' ;
    my $sthConsulta = $dbh->prepare( $sqlConsulta );## Preparar la sentencia de insercion en la base de datos
    $sthConsulta->execute();
    my $compradoEvento = "null";
    my $compradoCiudad = "null";
    my $compradoFecha = "null";
    my $compradoHora = "null";
    my $compradoLugar = "null";
    
    while (my @row = $sthConsulta->fetchrow_array) 
    { 
      $compradoEvento = $row[0];
      $compradoCiudad = $row[1];
      $compradoFecha   = $row[2];
      $compradoHora = $row[3];
      $compradoLugar = $row[4];
    }

print '
<div class="modal fade" id="myModalCompra" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Evento</h4>
      </div>
      <div class="modal-body">
         <form role="form" action="index.cgi?comprado=true" method="post">
              <div class="form-group" >
                <label class="col-sm-4 control-label" for="">Evento</label>
                <div class="col-sm-8 ">
                  <input type="text" class="form-control"  placeholder="" name="evento" value="'.$compradoEvento.'"  disabled>
                </div>
              </div>
              <div class="form-group ">
                <label class="col-sm-4 control-label" for="">Fecha</label>
                <div class="col-sm-8 ">
                <input type="text" class="form-control"  placeholder="" name="ciudad" value="'.$compradoCiudad.'"  disabled>
                </div>
              </div>
              <div class="form-group ">
                <label class="col-sm-4 control-label" for="">Lugar</label>
                <div class="col-sm-8 ">
                <input type="text" class="form-control"  placeholder="" name="foro"  value="'.$compradoLugar.'"  disabled>
                </div>
              </div>
              <div class="form-group ">
                <label class="col-sm-4 control-label" for="">Hora</label>
                <div class="col-sm-8 ">
                <input type="text" class="form-control"  placeholder="" name="fecha"  value="'.$compradoFecha.'"  disabled>
                </div>
              </div>
              <div class="form-group ">
                <label class="col-sm-4 control-label" for="">Ciudad</label>
                <div class="col-sm-8 ">
                <input type="text" class="form-control"  placeholder="" name="hora"  value="'.$compradoHora.'"  disabled>
                </div>
              </div>
              <!--div class="form-group ">
                <label class="col-sm-4 control-label" for="">Tipo Boleto</label>
                <div class="col-sm-8 ">
                  <select class="form-control" name="tipoBoleto">
                    <option>Adulto</option>
                    <option>Niño</option>
                    <option>Adulto mayor</option>
                  </select>
                </div>
              </div-->
              <div class="form-group ">
                <label class="col-sm-4 control-label" for="">Seccion</label>
                <div class="col-sm-8 ">
                  <select class="form-control" name="seccion">';
    
    my $sqlConsulta = 'SELECT seccion.nombre,seccion.precio FROM evento INNER JOIN evento_has_foro ON evento_has_foro.evento_nombre = evento.nombre 
INNER JOIN foro ON foro.nombre = evento_has_foro.foro_nombre INNER JOIN seccion ON seccion.foro_nombre = foro.nombre  WHERE evento.nombre = 
"'.$evento.'" ' ;
    my $sthConsulta = $dbh->prepare( $sqlConsulta );## Preparar la sentencia de insercion en la base de datos
    $sthConsulta->execute();
    
    while (my @row = $sthConsulta->fetchrow_array) 
    {    print '<option >'.$row[0].'</option>';
    }
                  print'
                  </select>
                </div>
              </div>
              <div class="form-group ">
                <label class="col-sm-4 control-label" for="">Precio</label>
                <div class="col-sm-8 ">';
    my $sqlConsulta = 'SELECT seccion.nombre, MAX(seccion.precio) FROM evento INNER JOIN evento_has_foro ON evento_has_foro.evento_nombre = 
evento.nombre INNER JOIN foro ON foro.nombre = evento_has_foro.foro_nombre INNER JOIN seccion ON seccion.foro_nombre = foro.nombre  WHERE 
evento.nombre = "'.$evento.'" ' ;
    my $sthConsulta = $dbh->prepare( $sqlConsulta );## Preparar la sentencia de insercion en la base de datos
    $sthConsulta->execute();
    
    while (my @row = $sthConsulta->fetchrow_array) 
    {   print '<input type="text" class="form-control" id="" placeholder="$" value="'.$row[1].'" name="precio">';

    }
                print '</div>
              </div>
              <div class="form-group ">
                <label class="col-sm-4 control-label" for="">Catidad Boletos</label>
                <div class="col-sm-8 ">
                  <select class="form-control" name="cantidad">
                    <option>1</option>
                    <option>2</option>
                    <option>3</option>
                  </select>
                </div>
              </div>
               <div class="form-group" >
                <label class="col-sm-4 control-label" for="">id Cliente</label>
                <div class="col-sm-8 ">
                  <input type="text" class="form-control" id="" placeholder=""  value="" name="cliente">
                </div>
              </div>
      </div>
      <div class="modal-footer">
              <button type="submit" class="btn btn-primary">COMPRAR</button>
            </form>
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->
';
    
}


    
print '
    <!-- Carousel
    ================================================== -->
    <div id="myCarousel" class="carousel slide" data-ride="carousel">
      <!-- Indicators -->

      <ol class="carousel-indicators">
        <li data-target="#myCarousel" data-slide-to="0" class="active"></li>
        <li data-target="#myCarousel" data-slide-to="1"></li>
      </ol>
      <div class="carousel-inner">
        <div class="item active">

          <img data-src="holder.js/900x500/auto/#555:#5a5a5a/text:Third slide" alt="Third slide">
          <img src="http://www.starwoodhotels.com/lemeridien/images/meetings/meetings_banner.jpg" 
data-src="http://www.starwoodhotels.com/lemeridien/images/meetings/meetings_banner.jpg" alt="slider">
          <div class="container">
            <div class="carousel-caption">
              <h1>Eample headline.</h1>
              <p></p>
              <p><a class="btn btn-lg btn-primary" href="admin" role="button">go admin</a></p>
            </div>
          </div>
        </div>
        <div class="item">
          <img data-src="http://www.f-covers.com/cover/music-dj-sampler-console-facebook-cover-timeline-banner-for-fb.jpg" 
src="http://www.f-covers.com/cover/music-dj-sampler-console-facebook-cover-timeline-banner-for-fb.jpg" alt="Second slide">
          <div class="container">
            <div class="carousel-caption">
              <!--h1>Another example headline.</h1>
              <p>Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id 
nibh ultricies vehicula ut id elit.</p>
              <p><a class="btn btn-lg btn-primary" href="#" role="button">Learn more</a></p-->
            </div>
          </div>
        </div>
        
      </div>
      <a class="left carousel-control" href="#myCarousel" data-slide="prev"><span class="glyphicon glyphicon-chevron-left"></span></a>
      <a class="right carousel-control" href="#myCarousel" data-slide="next"><span class="glyphicon glyphicon-chevron-right"></span></a>
    </div><!-- /.carousel -->';


#BUSQUEDA POR SUBCATEGORIA 
my $dbh = DBI->connect("dbi:mysql:themach2_ticketmaster", 'themach2_usuario', 'optiplex') or die "Error de conexion: \n";

print '<div id="x"> </div>';
if($VariablesGet{'search'}  eq "subcategoria")
{
$subcategoria = $VariablesGet{'subcategoria'};  
my $sqlConsulta = 'SELECT evento.nombre, evento.fecha, evento.hora, evento.imagenUrl, foro.nombre, ciudad.nombre, estado.nombre FROM categoria INNER 
JOIN subcategoria ON subcategoria.categoria_nombre = categoria.nombre INNER JOIN evento ON evento.subcategoria_nombre = subcategoria.nombre INNER JOIN 
evento_has_foro ON evento_has_foro.evento_nombre = evento.nombre INNER JOIN foro ON foro.nombre = evento_has_foro.foro_nombre INNER JOIN ciudad ON 
ciudad.id = foro.ciudad_id INNER JOIN estado ON estado.id = ciudad.estado_id WHERE subcategoria.nombre =  "'.$subcategoria.'"'; #print $sql2;
my $sthConsulta = $dbh->prepare( $sqlConsulta );## Preparar la sentencia de insercion en la base de datos
$sthConsulta->execute();
while (my @row = $sthConsulta->fetchrow_array) 
{ 
                      
print'
<hr class="featurette-divider ">
<div class="resultadosSubCategoria" >
<div class="container">
<div class="row featurette ">
  <div class="table-responsive">
                  <table class="table">
                    <thead>
                        <th>Thumbnail</th>
                        <th>Evento</th>
                        <th>Lugar</th>
                        <th>Fecha</th>
                        <th>Enlace</th>
                    </thead>
                    <tbody>
                      <tr>
                        <td><a href="index.cgi?search=evento&evento='.$row[0].'#resultados"><img style="max-width:100px" class="img-thumbnail center 
img-responsive" data-src="'.$row[0].'" alt="100x100" src="'.$row[3].'"></a></td>
                        <td><a href="index.cgi?search=evento&evento='.$row[0].'#resultados"><h1>'.$row[0].'</h1></a></td>
                        <td><b>'.$row[4].'</b><br>'.$row[5].' '.$row[6].'</td>
                        <td>'.$row[1].' / '.$row[2].'</td>
                        <td><a class="label label-primary" href="index.cgi?search=evento&evento='.$row[0].'#resultados">Busca tus Boletos</a> </td>
                </tr>
			</tbody>
		</table>
	</div>
</div>
</div><!--resultadosSubCategoria-->
</div>
';
}
}

#DETALLE EVENTO SELECCIONADO
if($VariablesGet{'search'} eq "evento")
{
	$evento = $VariablesGet{'evento'};  
	my $sqlConsulta = 'SELECT evento.nombre, evento.fecha , evento.hora , evento.imagenUrl, foro.nombre  FROM categoria  INNER JOIN subcategoria 
ON subcategoria.categoria_nombre = categoria.nombre  INNER JOIN evento ON evento.subcategoria_nombre = subcategoria.nombre INNER JOIN evento_has_foro 
ON evento_has_foro.evento_nombre = evento.nombre INNER JOIN foro ON foro.nombre = evento_has_foro.foro_nombre  WHERE evento.nombre = "'.$evento.'"  '; 
#print $sql2;
	my $sthConsulta = $dbh->prepare( $sqlConsulta );## Preparar la sentencia de insercion en la base de datos
	$sthConsulta->execute();
	while (my @row = $sthConsulta->fetchrow_array) 
	{ 
	                      
	print'
	<hr class="featurette-divider ">
	<div id="resultados" class="resultadoEvento">
	<div class="container">
	<div class="row featurette ">
	   <div class="col-md-8">
	          <h1 class="featurette-heading">Evento : '.$row[0].' </h1><h2 class="text-muted">Lugar : '.$row[4].'</h2>
	          <p class="lead">Fecha : '.$row[1].'</p><p>Hora : '.$row[2].'</p>
            <a class="btn btn-success" href="index.cgi?compra=true&evento='.$row[0].'">Comprar</a>

	    </div>
	    <div class="col-md-4">
	          <img class="featurette-image img-responsive" data-src="'.$row[0].'" alt="500x500" src="'.$row[3].'">
	    </div>

  
	</div>
	</div><!-resultadoEvento-->
	</div>
	';
	}
}





print '<hr class="featurette-divider ">';
print '<style>.img-circle {max-width: 200px;-webkit-filter: grayscale(1);cursor:pointer} </style>';
print '<style>.img-circle:hover {-webkit-filter: none;}</style>';
print'
    
</div>';


require ("footer.cgi"); #add header


