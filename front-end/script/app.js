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
    // getTempHistory();
  });

  socket.on("B2F_meting_ldr", function (jsonObject) {
    console.log((jsonObject.waarde / 950) * 100, "%");
    const ldr = document.querySelector(".js-ldr").innerHTML = `lichtintensiteit: ${((jsonObject.waarde / 950) * 100).toFixed(2)}%`; //{((jsonObject.waarde /1023)*100)}
    ldr.innerHTML = jsonObject.waarde

    // # print("Waarde = {0:.2f}".format((channeldata/950)*100))
  });

  socket.on("B2F_temp_sens", function (jsonObject) {
    const temp = document.querySelector(".js-temp")
    temp.innerHTML = jsonObject["waarde"] //jsonObject.waarde 
    console.log(jsonObject, "°C");
    document.querySelector(".js-socket-temp").innerHTML = `temperatuur: ${jsonObject.waarde}°C`;
    getTempHistory();
  });

  socket.on("B2F_ph_sens", function (jsonObject) {
    console.log(jsonObject.waarde, "ph");
    const ph = document.querySelector(".js-ph").innerHTML = `ph waarde: ${jsonObject.waarde}`;
    ph.innerHTML = jsonObject.waarde
  });
};

const showLineHome = function (jsonObject) {
  let htmlString = "";
  console.log("KOMT HIER NIET IN1")
  for (i in jsonObject) {
    temp = jsonObject[i];
    let vorigeTemp = 0;
    vorigeTemp = jsonObject[i - 1];
    if (i == 0) {
      vorigeTemp = 0;
    } else {
      vorigeTemp = vorigeTemp.temp;
    }
    console.log("KOMT HIER NIET IN2")

    htmlString += `<tr style="--start: ${(vorigeTemp / 100) * 2}; --size: ${(temp.temp / 100) * 2}"><td><span class="data">${temp.temp}</span></td></tr>`;
  }
  htmlTableLineHome.innerHTML = htmlString;
  console.log("KOMT HIER NIET IN3")
};

const getTempHistory = function () {
  handleData(socket + "/api/v1/temp", showLineHome); //"http://192.168.0.236:5000/api/v1/temp"
  // console.log(getTempHistory)
};

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
  listenToUI();
  listenToSocket();
  console.info("after");
  htmlTableLineHome = document.querySelector(".js-line-table-home");
  listenToUI();
  listenToSocket();
});