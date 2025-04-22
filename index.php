<?php
    $path = rtrim(str_replace('\\','/',dirname($_SERVER['PHP_SELF'])), '/');
    $url = ((isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] == 'on') ? 'https://' : 'http://' ) . $_SERVER['HTTP_HOST'] . $path;
    header('X-Frame-Options: DENY');
?>
<!DOCTYPE html>
<html lang="es">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="description" content="Sistema de Gestión de Órdenes de Servicio TecnoComputer">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title>TecnoComputer - Sistema de Gestión</title>

        <link rel="icon" type="image/x-icon" href="<?=$url ?>/images/icon.png">
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.15.4/css/all.css">
        <link rel="stylesheet" href="<?=$url ?>/style.css">
    </head>
    <body>
        <!-- Header -->
        <header class="header">
            <div class="header-content">
                <div class="logo">
                    <img src="<?=$url ?>/images/logo.png" alt="TecnoComputer Logo">
                    <h1>TecnoComputer</h1>
                </div>
            </div>
        </header>

        <!-- Contenido Principal -->
        <div class="container">
            <div class="table-container">
                <table id="ordenesServicioTable">
                    <thead>
                        <tr>
                            <th>ID Orden</th>
                            <th>ID Cliente</th>
                            <th>Fecha Entrada</th>
                            <th>Inicio Trabajo</th>
                            <th>Fin Trabajo</th>
                            <th>Tiempo</th>
                            <th>Estado</th>
                            <th>Diagnóstico Final</th>
                            <th>Marca</th>
                            <th>Modelo</th>
                            <th>Serial</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td colspan="11" class="text-center">Cargando datos...</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <script>
            opensupports_version = '4.11.0';
            root = "<?=$url ?>";
            apiRoot = '<?=$url ?>/api';
            globalIndexPath = "<?=$path ?>";
            showLogs = false;
        </script>
        <?php if (preg_match('~MSIE|Internet Explorer~i', $_SERVER['HTTP_USER_AGENT']) || (strpos($_SERVER['HTTP_USER_AGENT'], 'Trident/7.0; rv:11.0') !== false)): ?>
          <script src="https://cdn.polyfill.io/v2/polyfill.min.js?features=String.prototype.startsWith,Array.from,Array.prototype.fill,Array.prototype.keys,Array.prototype.find,Array.prototype.findIndex,Array.prototype.includes,String.prototype.repeat,Number.isInteger,Promise&flags=gated"></script>
        <?php endif; ?>
        <script src="<?=$url ?>/bundle.js"></script>
    </body>
</html>
