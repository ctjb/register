function recalc() {
	var price = 50;
	var level = $('input[name=level]:checked').val();
	if (level === 'starving') {
		price = 0;
		$('#desc').show();
	} else {
		$('#desc').hide();
	}
	if (level === 'sponsor') {
		price = 100;
	}
	if ($('#tshirt').find('option:selected').val() != 'shirt-no') {
		price += 15;
	}
	$('#price').text(price);
}

$(function(){

	$('#level_starving').change(function(){ recalc(); });
	$('#level_regular').change(function(){ recalc(); });
	$('#level_sponsor').change(function(){ recalc(); });

	$('#tshirt').change(function(){ recalc(); });

});
