<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<title>Placement of Bootstrap 4 Tooltip via Data Attributes</title>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
<style>
	.bs-example{
    	margin: 100px 60px;
    }
</style>
<script>
    $(document).ready(function(){
        $('[data-toggle="tooltip"]').tooltip();
    });
</script>
</head>
<body>
<div class="bs-example"> 
    <ul class="list-inline">
        <li class="list-inline-item">
            <a href="#" data-toggle="tooltip" data-placement="top" title="Default tooltip">Tooltip</a>
        </li>
        <li class="list-inline-item">
            <a href="#" data-toggle="tooltip" data-placement="right" title="Another tooltip">Another tooltip</a>
        </li>
        <li class="list-inline-item">
            <a href="#" data-toggle="tooltip" data-placement="bottom" title="A much longer tooltip to demonstrate the max-width of the Bootstrap tooltip.">Large tooltip</a>
        </li>
        <li class="list-inline-item">
            <a href="#" data-toggle="tooltip" data-placement="left" title="The last tip!">Last tooltip</a>
        </li>
    </ul>
</div>
</body>
</html>                            