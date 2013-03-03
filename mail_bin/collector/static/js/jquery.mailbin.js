(function( $ ){

    $.fn.mailbinForm = function( options ) {

        var cbSuccess = false;

        // Create some defaults, extending them with any options that were provided
        var settings = $.extend( {
            'timeout'         : 5000,
            'background-color' : 'blue'
        }, options);

        return this.each(function() {

            $(this).submit(function(){

                var $this = $(this);
                $this.find('.text-success').text('');
                $this.find('.text-error').text('');

                // minimal check
                var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
                if (!re.test($(this).find('input[name=email]').val())) {
                    $this.find('.control-group').addClass('error');
                    return false;
                }
                // create an AJAX call...
                $.ajax({
                    data: $this.serialize(), // get the form data
                    type: 'GET', // jsonp wants GET type
                    dataType: 'jsonp', crossDomain: true,
                    url: $this.attr('action')
                }).done(function(data){
                        cbSuccess = true;
                        //var containerEl = $('#subscription_form');
                        if (data.errors) {
                            var txt = '';
                            for (var field in data.errors) {
                                for (var ix=0; ix < data.errors[field].length; ix++){
                                    txt += data.errors[field][ix] + '<br/>';
                                }
                            }
                            $this.find('.text-error').html(txt)
                        }
                        else {
                            $this.find('.control-group').removeClass('error');
                            $this.find('.text-success').html(data.result);
                            $this.find('.text-error').text('');
                        }
                    });
                // fix: fail/error method not work for jsonp requests
                setTimeout(function(){
                    if(!cbSuccess) { $this.find('.text-error').text("Il server non risponde, prova di nuovo."); }
                    else {
                        cbSuccess=false; // to allow new requests
                    }
                }, settings.timeout); // assuming 5sec is the max wait time for results
                return false;

            });

        });

    };
})( jQuery );