function chooseOption(optionIndex) {
    //
}

function setupScene(sceneData) {
    $('#navText').html(sceneData.description)
    sceneData.options.forEach((item, index) => {
        $('#optionsList').empty()
        $('<a>', {
            href: '#',
            class: 'list-group-item list-group-item-action',
            text: item.text,
            click: function (event) {
                event.preventDefault()
                chooseOption(index)
            }
        }).appendTo('#optionsList')
    })
}

function changeAttributeValue(target, delta) {
    $(target).html(function (_, oldHtml) {
        var value = +oldHtml
        return value + delta
    })
}

function setupAttributes(playerData) {
    currentStats = playerData.current_stats
    for (var stat in currentStats) {
        if (Object.prototype.hasOwnProperty.call(currentStats, stat)) {
            let tableRow = $('<tr>')
            $('<td>', { text: stat }).appendTo(tableRow)
            let valueCell = $('<td>')
            valueCell.appendTo(tableRow)
            $('<button>', {
                class: 'btn btn-sm btn-outline-danger',
                click: function (event) {
                    event.preventDefault()
                    changeAttributeValue(`#${stat}Value`, -1)
                }
            }).appendTo(valueCell)
            $('span', { id: `${stat}Value`, text: currentStats[stat] }).appendTo(valueCell)
            $('<button>', {
                class: 'btn btn-sm btn-outline-success',
                click: function (event) {
                    event.preventDefault()
                    changeAttributeValue(`#${stat}Value`, +1)
                }
            }).appendTo(valueCell)
        }
    }
}

function initPage(playerData) {
    setupAttributes(playerData)
    let currentScene = playerData.current_scene
    $.ajax(`/adventure/scene/${currentScene}`, {
        dataType: 'json',
        method: 'POST',
        success: function (data, _, _) {
            setupScene(data)
        },
        error: function (_, _, errorThrown) {
            $('#errorMessage').html(`Error occurred on /player request: ${errorThrown}`)
        }
    })
}

$(document).ready(function () {
    $.ajax('/player', {
        dataType: 'json',
        success: function (data, _, _) {
            initPage(data)
        },
        error: function (_, _, errorThrown) {
            $('#errorMessage').html(`Error occurred on /player request: ${errorThrown}`)
        }
    })
})
