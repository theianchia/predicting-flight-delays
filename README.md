<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Predicting Flight Delays</h3>

  <p align="center">
    How can we better predict flight delays?
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>


## About The Project


<p align="right">(<a href="#top">back to top</a>)</p>


## Data Preprocessing

### Columns
* Initial columns from raw airlines dataset

`FL_DATE` = Date of the Flight<br>
`OP_CARRIER` = Airline Identifier<br>
`OP_CARRIER_FL_NUM` = Flight Number<br>
`ORIGIN` = Starting Airport Code<br>
`DEST` = Destination Airport Code<br>
`CRS_DEP_TIME`= Planned Departure Time<br>
`DEP_TIME` = Actual Departure Time<br>
`DEP_DELAY` = Total Delay on Departure in minutes<br>
`TAXI_OUT` = The time duration elapsed between departure from the origin airport gate and wheels off<br>
`WHEELS_OFF` = The time point that the aircraft's wheels leave the ground<br>
`WHEELS_ON` = The time point that the aircraft'ss wheels touch on the ground<br>
`TAXI_IN` = The time duration elapsed between wheels-on and gate arrival at the destination airport<br>
`CRS_ARR_TIME` = Planned arrival time<br>
`ARR_TIME` = Actual Arrival Time = ARRIVAL_TIME - SCHEDULED_ARRIVAL<br>
`ARR_DELAY` = Total Delay on Arrival in minutes<br>
`CANCELLED` = Flight Cancelled (1 = cancelled)<br>
`CANCELLATION_CODE` = Reason for Cancellation of flight: A - Airline/Carrier; B - Weather; C - National Air System; D - Security<br>
`DIVERTED` = Aircraft landed on different airport that the one scheduled<br>
`CRS_ELAPSED_TIME` = Planned time amount needed for the flight trip<br>
`ACTUAL_ELAPSED_TIME` = AIR_TIME+TAXI_IN+TAXI_OUT<br>
`AIR_TIME` = The time duration between wheels_off and wheels_on time<br>
`DISTANCE` = Distance between two airports<br>
`CARRIER_DELAY` = Delay caused by the airline in minutes<br>
`WEATHER_DELAY` = Delay caused by weather<br>
`NAS_DELAY` = Delay caused by air system<br>
`SECURITY_DELAY` = caused by security reasons<br>
`LATE_AIRCRAFT_DELAY` = Delay caused by security<br>

<p align="right">(<a href="#top">back to top</a>)</p>


## EDA


<p align="right">(<a href="#top">back to top</a>)</p>
