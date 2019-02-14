        $(document).ready(function() {
            //POST a blank data to server for initalize
            $.ajax({ 
                url: '/input',
                data: '{"user_input":"initalize-welcome"}',
                type: 'POST',
                contentType: 'application/json',
                dataType: 'json',
                success: function(results)
                {
                    results.forEach(result => {
                            $string = '<div class="chatbot_dialogue"><span>chatbot: ' + result['text'] + '</span></div>';
                        $('#flow_id').append($string);
                    });
                }
            });
            //Send POST request when onclick
            $("#sendbutton_id").click(function(){
                var $string = "";
                var $input_text = $("#textfield_id").val();
                document.getElementById('textfield_id').value = "";
                console.log($input_text);
                if ($input_text == "") {
                    alert("Cannot be empty!");
                    return;
                }
                else {
                    $string = '<div class="student_dialogue"><span>Student: ' + $input_text + '</span></div>';
                    $('#flow_id').append($string);
                    if (typeof($input_text)=="string"){
                        $input_text = '"'+$input_text+'"'
                    }
                }
                $.ajax
                ({ 
                    url: '/input',
                    data: '{"user_input":'+$input_text+'}',
                    type: 'POST',
                    contentType: 'application/json',
                    dataType: 'json',
                    success: function(results)
                    {
                        results.forEach(result => {
                            switch (result['response_type']){
                                case "text":
                                    $string = '<div class="chatbot_dialogue"><span>chatbot: ' + result['text'] + '</span></div>';  
                                    break;
                                case "image":
                                    $string= '<div class="chatbot_dialogue"><span>chatbot: <img src="'+result['source']+'"></span></div>';
                                    break;
                                default:
                                    $string = '<div class="chatbot_dialogue"><span>chatbot: Hello </span></div>';  
                                    break;
                            }
                            $('#flow_id').append($string);
                        });
                    },
                    error: function(){
                        alert("Cannot connect to server!");
                    }
                });
            });
        });