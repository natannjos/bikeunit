window.BikeUnit = {}
window.BikeUnit.inicializa = function(){
    $('input[name="destino"]').on('keypress', function(){
        $('.has-error').hide()
    });
}