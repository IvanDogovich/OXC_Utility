<?PHP
/**
 * Index.php - loads globals
 *
 * @package     starvingpoet.net
 * @subpackage  master
 * @author      Nick Green - <starvingpoet@clan-quant.net>
 * @copyright   2010
 * @filesource
 *
 * @version 2010.01.20 - Initial Creation
 */

if (strpos($_SERVER['REMOTE_ADDR'],'192.168.1') === false && strpos($_SERVER['REMOTE_ADDR'],'127.0.0.1') === false)
{
    ECHO "<h1>Site undergoing upgrades, check back in a bit</h1><p>-Poet</p>";
    exit();
}

set_time_limit(0);
include_once("library/include.inc");


if (isset($_REQUEST["a"]))
{
   	include("ajax.php");
}
else if (isset($_REQUEST["s"]))
{
    include("script.php");
}
else
{
    include("page.php");
}

?>