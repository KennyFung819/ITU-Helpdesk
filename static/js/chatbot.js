        $(document).ready(function() {
            var $current_lang = "en";
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
                            $string = '<div class="chatbot_dialogue"><span>Helpdesk: ' + result['text'] + '</span></div>';
                        $('#flow_id').append($string);
                    });
                }
            });
            //Send POST request when onclick
            $("#translatebutton_id").click(function(){
                $lang_selected = $( "#translate_selection" ).val();
                switch ($lang_selected){
                    case "English":
                        $current_lang = "en";
                        break;
                    case "Spanish":
                        $current_lang = "en-es";
                        break;
                    case "Germany":
                        $current_lang = "en-de";
                        break;
                    case "Japanese":
                        $current_lang = "en-ja";
                        break;
                    case "Russian":
                        $current_lang = "en-ru";
                        break;
                    case "Chinese":
                        $current_lang = "en-zh"
                }
            })
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
                    $string = '<div class="student_dialogue"><span> You: ' + $input_text + '</span></div>';
                    $('#flow_id').append($string);
                    if (typeof($input_text)=="string"){
                        $input_text = '"'+$input_text+'"'
                    }
                }
                $.ajax({ 
                    url: '/input',
                    data: '{"user_input":'+$input_text+'}',
                    type: 'POST',
                    contentType: 'application/json',
                    dataType: 'json',
                    success: function(assistantResults)
                    {
                        assistantResults.forEach(result => {
                            switch (result['response_type']){
                                case "text":
                                    if ($current_lang == 'en'){
                                        $string = '<div class="chatbot_dialogue"><span>Helpdesk: ' + result['text'] + '</span></div>';  
                                        $('#flow_id').append($string);
                                    }
                                    else{
                                        console.log(result['text']);
                                        trim_string = result['text'].replace(/(\r\n|\n|\r)/gm, ""); 
                                        console.log(trim_string);                
                                        $.ajax({ 
                                            url: '/translate',
                                            data: '{"model_id":"'+$current_lang+'","text":"'+trim_string+'"}',
                                            type: 'POST',
                                            contentType: 'application/json',
                                            dataType: 'text',
                                            success: function(translateResult)
                                            {
                                                $string = '<div class="chatbot_dialogue"><span>Helpdesk: ' + translateResult + '</span></div>';
                                                $('#flow_id').append($string);                                          
                                            }
                                        });
                                    }
                                    break;
                                case "image":
                                    $string= '<div class="chatbot_dialogue"><span>Helpdesk: <img src="'+result['source']+'"></span></div>';
                                    $('#flow_id').append($string);
                                    break;
                                default:
                                    $string = '<div class="chatbot_dialogue"><span>Helpdesk: Hello </span></div>'; 
                                    $('#flow_id').append($string); 
                                    break;
                            }
                        });
                    },
                    error: function(){
                        alert("Cannot connect to server!");
                    }
                });
            });
        });