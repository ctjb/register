function recalc() {
	var price = 40;
	if ($('#tshirt').find('option:selected').val() != 'shirt-no') {
		price += 15;
	}
	$('#price').text(price);
}

$(function(){
	$('#tshirt').change(function(){ recalc(); });
});
