/**
 * Created by mjwunderlich on 9/14/18.
 */
$(function () {
    function get_width_and_height() {
        var width = $('[name=width]').val();
        var height = $('[name=height]').val();

        return {
            'width': width,
            'height': height
        };
    }

    function unique_id() {
        var buffer = "";
        var max_length = 12;
        var i;

        for (i = 0; i < max_length; ++i)
            buffer += ('' + Math.floor(Math.random() * 9));

        return buffer;
    }

    $('#submit').click(function (e) {
        e.preventDefault();
        var dimensions = get_width_and_height();
        var width = dimensions['width'];
        var height = dimensions['height'];
        var no_cache = unique_id();
        var url = '/imagegen/mandelbrot/' + width + 'x' + height + '?no_cache=' + unique_id();

        $.ajax({
            url: url,
            type: 'get',
            success: function (response) {
                console.log(response);
                var image_url = '/imagegen/saved/' + response.url;
                $('#outer-container')
                    .css({
                        background: 'transparent url(\'' + image_url + '\') no-repeat scroll center center',
                        backgroundSize: 'cover'
                    });

                $('#download-image').attr('href', image_url).show();

                window.location.href = '/' + response.url;
            }
        });
    });

    $('#myMosaic').Mosaic();
});
