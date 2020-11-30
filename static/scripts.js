
let $switchPortsTable = $('#switchPortsTable');
let formQueryResultDiv = document.getElementById("formQueryResultDiv")

$(document).on("click", "#findIpAddButton", function(event){
    formQueryResultDiv.innerHTML = "";
    event.preventDefault();
    let ip_address = $('#inputIpAddress').val();
    console.log(ip_address);
    $.ajax({
        url: "/switch_ports.json",
        type: "POST",
        data: JSON.stringify(ip_address),
        dataType: "json",
        contentType: "application/json",
        success: function(data) {
            $switchPortsTable.bootstrapTable("destroy");
            $switchPortsTable.bootstrapTable({data: data.host_ports})
            formQueryResultDiv.innerHTML = "MAC Address: " + data.arp[0];

        }
    });
});