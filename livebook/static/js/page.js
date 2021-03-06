function chooseOption(optionIndex) {
    $.ajax(`/adventure/next/${optionIndex}`, {
        dataType: 'json',
        success: function (data, _, _) {
            setupScene(data)
        },
        error: function (_, _, errorThrown) {
            console.error(`Error occurred on /adventure/next request: ${errorThrown}`)
        }
    })
}

function setupScene(sceneData) {
    $('#navText').html(sceneData.description.replace(/\n/g, '<br>'))
    $('#optionsList').empty()
    sceneData.options.forEach((item, index) => {
        $('<a>', {
            href: '#',
            class: 'list-group-item list-group-item-action',
            text: item.text,
            click: function (event) {
                event.preventDefault()
                chooseOption($(this).attr('data-option-index'))
            },
            'data-option-index': index
        }).appendTo('#optionsList')
    })
}

function changeAttributeValue(statAlias, delta) {
    target = `#${statAlias}`
    $(target).html(function (_, oldHtml) {
        let oldValue = +oldHtml
        let newValue = Math.max(0, oldValue + delta)

        oathIndex = Math.min(newValue, $(this).attr('data-max'))
        $(`.${statAlias}-oath`).hide()
        $(`#${statAlias}-oath-${oathIndex}`).show()

        let operation = delta >= 0 ? 'increase' : 'decrease'
        let attributeAlias = $(target).attr('data-alias')
        $.ajax(`/${operation}/${attributeAlias}`, {
            method: 'POST',
            error: function (_, _, errorThrown) {
                console.log(`Could not change attribute because of ${errorThrown}`)
            }
        })
        return newValue
    })
}

function setupAttributes(statsData) {
    $('#attributeTable').empty()
    statsData.forEach(stat => {
        const tableRow = $('<tr>')
        tableRow.appendTo('#attributeTable')
        $('<td>', { text: stat.name }).appendTo(tableRow)
        const valueCell = $('<td>')
        valueCell.appendTo(tableRow)
        $('<button>', {
            class: 'btn btn-sm btn-outline-danger',
            click: function (event) {
                event.preventDefault()
                changeAttributeValue($(this).attr('data-target'), -1)
            },
            'data-target': `${stat.alias}`,
            text: '-'
        }).appendTo(valueCell)
        $('<span>', {
            id: `${stat.alias}`,
            text: stat.default_value,
            'data-alias': stat.alias,
            'data-max': stat.oaths.length - 1,
            // I know using style attribute is bad
            // By using it I confirm that I am a bad programmer
            // I should not use style attribute
            // Especially in JS code
            style: 'width: 2.5rem; display: inline-block; text-align: center;'
        }).appendTo(valueCell)
        $('<button>', {
            class: 'btn btn-sm btn-outline-success',
            click: function (event) {
                event.preventDefault()
                changeAttributeValue($(this).attr('data-target'), +1)
            },
            'data-target': `${stat.alias}`,
            text: '+'
        }).appendTo(valueCell)
    })
    $.ajax('/player', {
        dataType: 'json',
        success: function (playerData, _, _) {
            statsData = playerData.current_stats
            for (var stat in statsData) {
                if (Object.prototype.hasOwnProperty.call(statsData, stat)) {
                    $(`#${stat}`).html(statsData[stat])
                }
            }
        },
        error: function (_, _, errorThrown) {
            console.error(`Error occurred on /player request: ${errorThrown}`)
        }
    })
}

function initPage(playerData) {
    const currentScene = playerData.current_scene
    $.ajax(`/adventure/scene/${currentScene}`, {
        dataType: 'json',
        success: function (sceneData, _, _) {
            setupScene(sceneData)
        },
        error: function (_, _, errorThrown) {
            console.error(`Error occurred on /adventure/scene request: ${errorThrown}`)
        }
    })
}

function setupOaths(adventureData) {
    const allOaths = $('<ul>').appendTo($('#navOaths'))
    adventureData.stats.forEach(stat => {
        // Index of an oath in the array is the stat value necessary to activate the oath
        stat.oaths.forEach((oath, targetStatValue) => {
            $('<li>', {
                class: `${stat.alias}-oath`,
                id: `${stat.alias}-oath-${targetStatValue}`,
                text: `${stat.name}: ${oath}`
            }).hide().appendTo(allOaths)
        })
        statValue = +$(`span#${stat.alias}`).text()
        console.log(statValue)
        oathIndex = Math.max(0, Math.min(statValue, stat.oaths.length - 1))
        console.log(oathIndex)
        $(`#${stat.alias}-oath-${oathIndex}`).show()
    })
}

$(document).ready(function () {
    $.ajax('/player', {
        dataType: 'json',
        success: function (playerData, _, _) {
            initPage(playerData)
        },
        error: function (_, _, errorThrown) {
            console.error(`Error occurred on /player request: ${errorThrown}`)
        }
    })
    $.ajax('/adventure', {
        dataType: 'json',
        success: function (adventureData, _, _) {
            setupAttributes(adventureData.stats)
            setupOaths(adventureData)
        },
        error: function (_, _, errorThrown) {
            console.error(`Error occurred on /adventure request: ${errorThrown}`)
        }
    })
})
