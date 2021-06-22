var myModal = new bootstrap.Modal(document.getElementById('myModal'), {
    backdrop: 'static',
    keyboard: true,
    focus: true,
})

myModal.show();

$(function() {
    var ctx = document.getElementById('myChart').getContext('2d');
    var ChartDate = [];
    var ChartData = [];
    var ChartData1 = [];
    //'rgba(255, 99, 132, 0.2)',
    //'rgba(54, 162, 235, 0.2)',
    //'rgba(255, 206, 86, 0.2)',
    //'rgba(75, 192, 192, 0.2)',
    //'rgba(153, 102, 255, 0.2)',
    //'rgba(255, 159, 64, 0.2)'
    var chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ChartDate,
            datasets: [{
                label: '獲利',
                data: ChartData,
                backgroundColor: [
                    'rgba(153, 102, 255, 0.2)',
                ],
                borderColor: [
                    'rgba(153, 102, 255, 0.2)',
                ],
                borderWidth: 1,
            },
            {
                label: '累積獲利',
                data: ChartData1,
                borderColor: [
                    'rgba(255, 159, 64, 0.2)'
                ],
                backgroundColor: [
                    'rgba(255, 159, 64, 1)'
                ],
                type: 'line',
                order: 0
            }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    //var myTables = $('#example').DataTable( {
    //    "paging":   true,
    //    "ordering": false,
    //    "language": {
    //        "info": "", // 表格左下角显示的文字
    //        "paginate": {
    //            "previous": "上一頁",
    //            "next": "下一頁"
    //        }
    //    },
    //    "destroy": true,
    //    "retrieve":true,
    //});

    $("#submit").on("click",function(){
        myModal.show();
        reques();
    })

    function reques(){
        let data = {
            "stock":$("#stock").val(),
            "sdate":$("#sdate").val(),
            "edate":$("#edate").val(),
            "D1":$("#D1:checked").length,
            "D2":$("#D2:checked").length,
            "C1":$("#C1:checked").length,
            "C2":$("#C2:checked").length,
            "C3":$("#C3:checked").length,
        };
        axios.post("/api/get_data",Qs.stringify(data))
        .then (res=>{
            let response = res['data'];
            var d = response['data'];
            console.log(response);
            clears();
            $('#tbody').html("");
            //mytables.clear().draw();
            d['售出時間'].forEach(function(val,i){
                ChartDate.push(d['售出時間'][i]);
                ChartData.push(d['獲利'][i]);
                ChartData1.push(d['累積獲利'][i]);
                chart.update();

                var text = "<tr>";
                text += "<td>"+d['買進時間'][i]+"</td>";
                text += "<td>"+d['買進價格'][i]+"</td>";
                text += "<td>"+d['買進原因'][i]+"</td>";
                text += "<td>"+d['售出時間'][i]+"</td>";
                text += "<td>"+d['售出價格'][i]+"</td>";
                text += "<td>"+d['售出原因'][i]+"</td>";
                text += "<td>"+d['數量'][i]+"</td>";
                text += "<td>"+d['獲利'][i]+"</td>";
                $('#tbody').append(text);
                
            });
            $("#tot").html(response['交易次數']);
            $("#totmoney").html(response['總盈虧']);
            setTimeout(function(){ myModal.hide(); }, 500);
        })
        .catch(err => {
            setTimeout(function(){ myModal.hide(); }, 500);
            console.error(err);   
        });
    }

    function clears(){
        var x = ChartDate.length;
        for(var i = 0; i <= x; i++){
            ChartDate.pop();
            ChartData.pop();
            ChartData1.pop();
        }
        $('#tbody').html();
        chart.update();
    }
    setTimeout(function(){ myModal.hide(); }, 700);
    reques();
} );