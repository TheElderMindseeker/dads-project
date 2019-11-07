function setupScene(sceneData) {
    $('#navText').html(sceneData.description)
    sceneData.options.forEach((item) => {
        $('#optionsList').empty()
        $('<a>', {href: '#', class: 'list-group-item list-group-item-action', text: item.text}).appendTo('#optionsList')
    })
}

function initPage(playerData) {
    let currentScene = playerData.current_scene
    $.ajax(`/adventure/scene/${currentScene}`, {
        dataType: 'json',
        method: 'POST',
        success: function(data, _, _) {
            setupScene(data)
        },
        error: function(_, _, errorThrown) {
            $('#errorMessage').html(`Error occurred on /player request: ${errorThrown}`)
        }
    })
}

$(document).ready(function () {
    $.ajax('/player', {
        dataType: 'json',
        success: function(data, _, _) {
            initPage(data)
        },
        error: function(_, _, errorThrown) {
            $('#errorMessage').html(`Error occurred on /player request: ${errorThrown}`)
        }
    })
})
