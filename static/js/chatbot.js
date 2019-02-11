<script type="text/javascript">

    $window.load(function () {
        var words = $("flow_id");
        var flow_id_in_the_field = $("textfield_id");
        var sendout = $("sendbutton_id");
        $('.sendout').click(function(){
            var string = "";
            var input_text = flow_id_in_the_field.value;
            if (input_text == "") {
                alert("Cannot be empty!");
                return;
            }
            else {
                string = '<div class="chatbot_dialogue"><span>Chatbot: ' + flow_id_in_the_field.value + '</span></div>';
                words.innerHTML = words.innerHTML + string;
            }
            $.ajax
            ({ 
                url: '127.0.0.1/input',
                data: {"user_input":input_text },
                type: 'post',
                dataType: "json",
                success: function(results)
                {
                    results.forEach(result => {
                        string = '<div class="student_dialogue"><span>Student: ' + flow_id_in_the_field.value + '</span></div>';     
                        words.innerHTML = words.innerHTML + string;                  
                    });
                }
            });
        });
    });
</script>