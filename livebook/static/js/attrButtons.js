$('.attr-reduce').on('click', function() {
    let target = $(this).data('target')
    $(target).html(function(_, oldHtml) {
        var value = +oldHtml
        return value - 1
    })
})

$('.attr-increase').on('click', function() {
    let target = $(this).data('target')
    $(target).html(function(_, oldHtml) {
        var value = +oldHtml
        return value + 1
    })
})
