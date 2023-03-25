document.getElementById('apiCallButton').addEventListener('click', async () => {
    const apiURL = 'https://mdbmtinu7h.execute-api.us-east-2.amazonaws.com/prod'; // Replace with your API Gateway Invoke URL
    const response = await fetch(apiURL);
    const responseData = await response.json();
    const responseBody = JSON.parse(responseData.body);
  
    // Extract individual values from the body
    const observationArray = responseBody.observation;
    const minDate = responseBody.feels_like.min_date;
    const maxDate = responseBody.feels_like.max_date;
    const averageDate = responseBody.feels_like.average_date;
  
    // Place the values into the corresponding HTML elements
    const observationContainer = document.getElementById('observationContainer');
    observationContainer.innerHTML = ''; // Clear previous content
    observationArray.forEach((observation, index) => {
      const observationElement = document.createElement('div');
      observationElement.id = `observation-${index}`;
      observationElement.textContent = observation;
      observationContainer.appendChild(observationElement);
    });
  
    document.getElementById('minDate').textContent = 'Based on the low temperature, today feels most similar to ' + minDate;
    document.getElementById('maxDate').textContent = 'Based on the high temperature, today feels most similar to ' + maxDate;
    document.getElementById('averageDate').textContent = 'Considering both the low and high temperatures, today feels most similar to ' + averageDate;
  });
  
  