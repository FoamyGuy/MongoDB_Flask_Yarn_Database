const URL_BASE = "/yarn";

const $yarnTableBody = document.querySelector("#yarn_table tbody");

async function fetchData() {
    const response = await fetch(URL_BASE);
    const yarn_data = await response.json();
    //console.log(todos);
    return yarn_data
}


function colorIntToHexStr(colorInt) {
    let hexStr = "";
    hexStr += colorInt.toString(16);
    return "#" + hexStr.padStart(6, "0");
}


function wrapWithEditLink(text, yarn_id) {
    let $newEditLink = document.createElement("a")
    $newEditLink.href = "/edit/yarn/" + yarn_id;
    $newEditLink.innerText = text;

    return $newEditLink;
}

function loadTable() {

    $yarnTableBody.innerHTML = "";
    fetchData().then(function (yarn_data) {
        console.log("inside then() temperature_data: " + yarn_data)
        for (let i = 0; i < yarn_data.length; i++) {
            let curYarnData = yarn_data[i];
            console.log(curYarnData);
            // let $newLi = document.createElement("li")
            // $newLi.innerText = curItem.done ? "[x]: " : "[ ]: " + curItem.task;
            // $todosList.append($newLi);
            let $newRow = document.createElement("tr");

            let $newTdColor = document.createElement("td");
            let hexColor = colorIntToHexStr(curYarnData.color);
            //$newTdColor.innerText = hexColor;
            $newTdColor.append(wrapWithEditLink(hexColor, curYarnData._id["$oid"]));
            $newTdColor.style.backgroundColor = hexColor;
            $newRow.append($newTdColor);

            let $newTdAmount = document.createElement("td");

            // let $newEditLinkAmount = document.createElement("a")
            // $newEditLinkAmount.href = "/edit/yarn/" + curYarnData._id["$oid"];
            // $newEditLinkAmount.innerText = curYarnData.amount;

            //$newTdAmount.innerText = curYarnData.amount;
            //$newTdAmount.append($newEditLinkAmount);
            $newTdAmount.append(wrapWithEditLink(curYarnData.amount, curYarnData._id["$oid"]));

            $newRow.append($newTdAmount);

            let $newTdNotes = document.createElement("td");
            //$newTdNotes.innerText = curYarnData.notes != undefined ? curYarnData.notes : "";
            $newTdNotes.append(wrapWithEditLink(curYarnData.notes !== undefined ? curYarnData.notes : "", curYarnData._id["$oid"]));
            $newRow.append($newTdNotes);

            $yarnTableBody.append($newRow);
        }

    });

}

loadTable();
