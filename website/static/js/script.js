const loginForm = document.getElementById("loginForm");
const signupForm = document.getElementById("signupForm");

if (signupForm) {
  // Add event listener for form submission
  signupForm.addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way
    console.log("signup function called");
    // Get the values from the input fields
    const username = document.getElementById("exampleInputName_1").value;
    const email = document.getElementById("exampleInputEmail_2").value;
    const password1 = document.getElementById("exampleInputpwd_2").value;
    const password2 = document.getElementById("exampleInputpwd_3").value;

    // Validate that the password and confirm password match
    if (password1 !== password2) {
      alert("Passwords confirm password did  not match!");
      return;
    }

    // Prepare the data to send
    const data = {
      username: username,
      email: email,
      password1: password1,
      password2: password2,
    };

    // Send the data to the backend using Fetch API
    fetch("/signup", {
      // Replace with your backend signup route
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data), // Send the data as JSON
    })
      .then((response) => response.json()) // Parse the response as JSON
      .then((data) => {
        if (data.success) {
          // Redirect to login or another page after successful signup
          window.location.href = "/login"; // Change this URL to your target
        } else {
          // Display an error message if signup fails
          alert("Signup failed: " + data.message);
        }
      })
      .catch((error) => {
        // Handle network or other errors
        console.error("Error:", error);
        alert("Something went wrong. Please try again.");
      });
  });
}

if (loginForm) {
  loginForm.addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    // Get the values from the input fields
    const email = document.getElementById("exampleInputEmail_2").value;
    const password = document.getElementById("exampleInputpwd_2").value;

    // Prepare the data to send
    const data = {
      email: email,
      password: password,
    };

    // Send the data to the backend using Fetch API
    fetch("/login", {
      // Replace with your backend login route
      method: "POST", // HTTP method
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data), // Send the data as JSON
    })
      .then((response) => response.json()) // Parse the response as JSON
      .then((data) => {
        if (data.success) {
          // Redirect to the dashboard or another page after successful login
          window.location.href = "/"; // Change this URL to your target
        } else {
          // Display an error message if login fails
          alert("Login failed: " + data.message);
        }
      })
      .catch((error) => {
        // Handle network or other errors
        console.error("Error:", error);
        alert("Something went wrong. Please try again.");
      });
  });
}
const addcitybutton = document.getElementById("addCityButton");
if (addcitybutton) {
  addcitybutton.addEventListener("click", function () {
    var cityName = document.getElementById("cityInput").value;
    console.log(cityName);

    if (cityName) {
      fetch("/add_city", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: "city_name=" + encodeURIComponent(cityName), // Make sure cityName is passed correctly
      })
        .then((response) => response.json())
        .then((data) => {
          document.getElementById("cityInput").value = "";
          alert(data.message); // Show the message returned by the server

          // Clear the input field after successful insert
        })
        .catch((error) => {
          alert("An error occurred: " + error);
        });
    } else {
      alert("Please enter a city name.");
    }
  });
}

function getWeather() {
  // Get the selected city from the dropdown
  const city = document.getElementById("citySelect").value.trim();

  // Make an API call to the Flask backend with the selected city
  fetch(`/weather?city=${city}`)
    .then((response) => response.json())
    .then((data) => {
      weather = data.weather;
      city_data = data.city;

      // const forecast = data.forecast.forecastday;
      // const weekData = forecast.map((day) => {
      //   // Extract date and icon
      //   const date = day.date;
      //   const icon = day.day.condition.icon;
      //   const temp = day.day.avgtemp_c;
      //   // Calculate the ISO week number
      //   const dateObj = new Date(date);
      //   const weekNumber = getDayOfWeek(dateObj);

      //   return { date, icon, weekNumber, temp };
      // });
      // const tweek = data.forecast.forecastday[6].date;
      // const tdateObj = new Date(tweek);
      // const week = getDayOfWeek(tdateObj);

      // const todaydata = {
      //   date: data.forecast.forecastday[6].date,
      //   wind: data.forecast.forecastday[6].day.maxwind_kph,
      //   humidity: data.forecast.forecastday[6].day.avghumidity,
      //   week: week,
      // };
      document.getElementById("tweek").innerText = city_data.day_of_week;
      document.getElementById("tdate").innerText = city_data.date;
      document.getElementById("tdesc").innerText = city_data.city;
      document.getElementById("ttime").innerText =
        new Date().toLocaleTimeString();
      document.getElementById("twind").innerText = city_data.wind_speed;
      document.getElementById("thumidity").innerText = city_data.humidity;
      //     const todaydta = document.getElementById("today_data");
      //     todaydta.innerHTML = `
      //     <h6 class="block nowday">${todaydata.week}</h6>
      //     <span class="block nowdate">${todaydata.date}</span>
      //     <span>Wind Speed: ${todaydata.wind} kph</span><br />
      //     <span>Humidity: ${todaydata.humidity}%</span><br />
      //     <span>${new Date().toLocaleTimeString()}</span>
      // `;

      weather.forEach((dt, index) => {
        console.log("getting inside");
        // Get the respective day container, icon, and temperature element
        // const dayContainer = document.getElementById(`day${index + 1}`);
        // const weekdayElement = document.getElementById(`weekday${index + 1}`);
        const iconElement = document.getElementById(`icon${index + 1}`);
        const tempElement = document.getElementById(`temp${index + 1}`);
        console.log(dt);
        // Ensure the element exists
        if (tempElement) {
          // weekdayElement.textContent = data.weekNumber; // Day of the week (e.g., 'fri')
          // iconElement.src = data.icon; // Set the icon
          tempElement.innerHTML = `${Math.floor(dt.toFixed(2))} <sup>°C</sup>`; // Set the temperature
        }
        if (dt < 10) {
          iconElement.src = "static/img/storm.png"; // Cold weather icon
        } else if (dt >= 10 && dt < 26) {
          iconElement.src = "/static/img/cloudy.png"; // Cold icon
        } else if (dt >= 26) {
          iconElement.src = "/static/img/weather.png"; // Cloudy weather icon
        }
      });
      // console.log("today weather", todaydata);
      // console.log("week data ", weekData);
      // console.log(data);
    })
    .catch((error) => console.error("Error:", error));
}

function getDayOfWeek(date) {
  const daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  return daysOfWeek[date.getDay()]; // date.getDay() returns a number between 0 (Sunday) and 6 (Saturday)
}

const logoutButton = document.getElementById("logout");
if (logoutButton) {
  // Add event listener to handle logout click
  logoutButton.addEventListener("click", function () {
    // Send a fetch request to logout endpoint (e.g., '/logout')
    fetch("/logout", {
      method: "POST", // Assuming you're using a POST method to log out
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "same-origin", // To send cookies along with the request
    })
      .then((response) => {
        if (response.ok) {
          // If the logout is successful, redirect or update the UI
          window.location.href = "/login"; // Redirect to login page or another route
        } else {
          // Handle error (if any)
          console.error("Logout failed");
        }
      })
      .catch((error) => {
        // Handle any network or unexpected errors
        console.error("Error during logout:", error);
      });
  });
}
