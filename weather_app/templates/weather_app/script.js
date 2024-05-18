const chatButtons = document.querySelectorAll('.chat-button');
      chatButtons.forEach(function(button){
        button.addEventListener('click', function(){
          var weather_data = '{{weather_data1}}';
          var prompt = button.textContent;
          console.log('Prompt', prompt);
          var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
          console.log('Prompt', prompt);
          console.log('Weather Data', weather_data);

          fetch('/get_ai_response', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ prompt: prompt, weather_data: weather_data}),
          })
          .then(response => response.json())
          .then(data => {
            console.log('Response:', data);
            var responseText = data.response;
            console.log('Response Text:', responseText);
            var chatResponseText = document.getElementById('chat-response-text');
            chatResponseText.innerHTML = '';

            document.getElementById('chat-response').style.display = 'block';

            // Use Typed.js to create the typing effect
            var typed = new Typed(chatResponseText, {
              strings: [responseText],
              typeSpeed: 35,
              contentType: 'html',
              showCursor: true,
              cursorChar:'_',
              cursorBlinking: true,
            });
          })
          .catch(error => {
            console.error('Error:', error);
          });
        });
      });