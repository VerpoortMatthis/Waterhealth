const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);


socket.on("connect_error", (err) => {
  console.log(`connect_error due to ${err.message}`);
});

let htmlTableLineHome

const clearClassList = function (el) {
  el.classList.remove("c-room--wait");
  el.classList.remove("c-room--on");
};

const listenToUI = function () {
  console.log("listening UI");
};

const listenToSocket = function () {
  console.log("listening");
  socket.on("connected", function () {
    console.log("verbonden met socket webserver");
  });

  socket.on("B2F_meting_ldr", function (jsonObject) {
    console.log((jsonObject.waarde / 950) * 100, "%");
    const ldr = document.querySelector(".js-ldr").innerHTML = `lichtintensiteit: ${((jsonObject.waarde / 950) * 100).toFixed(2)}%`; //{((jsonObject.waarde /1023)*100)}
    ldr.innerHTML = jsonObject.waarde
    getphHistory();

    // # print("Waarde = {0:.2f}".format((channeldata/950)*100))
  });

  socket.on("B2F_temp_sens", function (jsonObject) {
    console.log("socket on B2F_temp_sens")
    const temp = document.querySelector(".js-temp")
    temp.innerHTML = jsonObject["waarde"] //jsonObject.waarde 
    console.log(jsonObject, "°C");
    // document.querySelector(".js-socket-temp").innerHTML = `temperatuur: ${jsonObject.waarde}°C`;
    getTempHistory();
  });

  socket.on("B2F_ph_sens", function (jsonObject) {
    console.log(jsonObject.waarde, "ph");
    const ph = document.querySelector(".js-ph").innerHTML = `ph waarde: ${jsonObject.waarde}`;
    ph.innerHTML = jsonObject.waarde
    getphHistory();
  });
};

const showLineHome = function (jsonObject) {
  let htmlString = "";
  for (i in jsonObject) {
    temp = jsonObject[i];
    let vorigeTemp = 0;
    vorigeTemp = jsonObject[i - 1];
    if (i == 0) {
      vorigeTemp = 0;
    } else {
      vorigeTemp = vorigeTemp.temp;
    }

    htmlString += `<tr style="--start: ${(vorigeTemp / 100) * 2}; --size: ${(temp.temp / 100) * 2}"><td><span class="data">${temp.temp}</span></td></tr>`;
  }
  htmlTableLineHome.innerHTML = htmlString;
};

const getTempHistory = function () {
  handleData(`http://${lanIP}/api/v1/temp`, Temp); ////"http://192.168.0.236:5000/api/v1/temp" `http://${lanIP}/api/v1/temp`
};

const getphHistory = function () {
  handleData(`http://${lanIP}/api/v1/ph`, Ph); ////"http://192.168.0.236:5000/api/v1/temp" `http://${lanIP}/api/v1/temp`
};

const getldrHistory = function () {
  handleData(`http://${lanIP}/api/v1/ldr`, Ldr); ////"http://192.168.0.236:5000/api/v1/temp" `http://${lanIP}/api/v1/temp`
};

const Temp = function (jsonObject) {
  data = {}
  let waardes = []
  console.log(waardes)
  for (let i of jsonObject) {
    let item = { x: i.datum, y: i.gemeten_waarde }
    waardes.push(item)
  }
  var options = {
    chart: {
      type: 'line',
      height: 350,
      animations: {
        enabled: true,
        speed: 1000
      }
    },
    series: [{
      data: waardes
    }],
    title: {
      text: 'huidig',
      align: 'left'
    },
    xaxis: {
      type: 'datetime',
    },
    yaxis: {
      max: 100
    },
    grid: {
      show: false
    },
    yaxis: {
      show: false
    },
    fill: {
      colors: ['#0067CD'],
    }
  }
  var chart = new ApexCharts(document.querySelector("#chart_temp"), options);

  chart.render();
}


const Ldr = function (jsonObject) {
  data = {}
  let waardes = []
  console.log(waardes)
  for (let i of jsonObject) {
    let item = { x: i.datum, y: i.gemeten_waarde }
    waardes.push(item)
  }
  var options = {
    chart: {
      type: 'line',
      height: 350,
      animations: {
        enabled: true,
        speed: 1000
      }
    },
    series: [{
      data: waardes
    }],
    title: {
      text: 'huidig',
      align: 'left'
    },
    xaxis: {
      type: 'datetime',
    },
    yaxis: {
      max: 950
    },
    grid: {
      show: false
    },
    yaxis: {
      show: false
    },
    fill: {
      colors: ['#0067CD'],
    }
  }
  var chart = new ApexCharts(document.querySelector("#chart_ldr"), options);

  chart.render();
}


const Ph = function (jsonObject) {
  data = {}
  let waardes = []
  console.log(waardes)
  for (let i of jsonObject) {
    let item = { x: i.datum, y: i.gemeten_waarde }
    waardes.push(item)
  }
  var options = {
    chart: {
      type: 'line',
      height: 350,
      animations: {
        enabled: true,
        speed: 1000
      }
    },
    series: [{
      data: waardes
    }],
    title: {
      text: 'huidig',
      align: 'left'
    },
    xaxis: {
      type: 'datetime',
    },
    yaxis: {
      max: 14
    },
    grid: {
      show: false
    },
    yaxis: {
      show: false
    },
    fill: {
      colors: ['#0067CD'],
    }
  }
  var chart = new ApexCharts(document.querySelector("#chart_ph"), options);

  chart.render();
}

const showTemperatuurData = function (jsonObject) {
  data = jsonObject.types
  console.log(data);

  let converted_labels = [];
  let converted_data = [];
  for (const item of data) {
    converted_labels.push((item.Tijd));
    converted_data.push((item.Meting + item.MeetEenheid));

  }
  drawChart(converted_labels, converted_data)
}

const listenToClickHistogram = function () {
  const buttons = document.querySelectorAll('.js-filter');
  for (const b of buttons) {
    b.addEventListener('click', function () {
      console.log('click filter');
      console.log(b.getAttribute('data-typeid'))
      currentTypeID = b.getAttribute('data-typeid');
      console.log('info ' + currentTypeID);
      handleData(`http://192.168.0.236:5000/api/v1/${currentTypeID}`, showTemperatuurData);
    });
  }
};

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  getTempHistory()
  getphHistory()
  getldrHistory()
  // getTempHistoryJuni()
  listenToUI();
  listenToSocket();
  console.info("after");
  htmlTableLineHome = document.querySelector(".js-line-table-home");
});



// const getTempHistoryJuni = function () {
//   handleData(`http://${lanIP}/api/v1/juni`, TempJuni); ////"http://192.168.0.236:5000/api/v1/temp" `http://${lanIP}/api/v1/temp`
// };

// const TempJuni = function (jsonObject) {
//   data = {}
//   let waardes = []
//   console.log(waardes)
//   for (let i of jsonObject) {
//     let item = { x: i.datum, y: i.gemeten_waarde }
//     waardes.push(item)
//   }
//   var options = {
//     chart: {
//       type: 'line',
//       height: 350,
//       animations: {
//         enabled: true,
//         speed: 1000
//       }
//     },
//     series: [{
//       data: waardes
//     }],
//     title: {
//       text: 'Juni',
//       align: 'left'
//     },
//     grid: {
//       show: false
//     },
//     yaxis: {
//       show: false
//     },
//     fill: {
//       colors: ['#0067CD'],
//     }
//   }
//   var chart = new ApexCharts(document.querySelector("#chart_tempJuni"), options);

//   chart.render();
// }
