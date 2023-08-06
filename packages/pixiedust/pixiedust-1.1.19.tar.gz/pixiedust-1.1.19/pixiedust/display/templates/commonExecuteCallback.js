{% macro ipython_execute(command, prefix, extraCommandOptions="{}", divId=None) -%}
{% set targetId=(divId if (divId and divId.startswith("$")) else ("'"+divId+"'") if divId else "'None'") %}
var callbacks = {
    shell : {
        reply : function(){
            if ( !callbacks.response ) {
                //Done executing
                {{caller('')}}
            }
        },
        payload : {
            set_next_input : function(payload){
                {% if this and this.options %}
                    var curCell=IPython.notebook.get_cells().filter(function(cell){return cell.cell_id=="{{this.options.get('cell_id')}}";});
                    curCell=curCell.length>0?curCell[0]:null;
                    if (!curCell){
                        console.log("Unable to execute set_next_input. Cell cannot be found");
                    }else{
                        curCell._handle_set_next_input(payload);
                    }
                {% else %}
                    console.log("Unable to execute set_next_input because context is not available. Perhaps you should import commonExecuteCallback.js with context");
                {% endif %}
            }
        }
    },
    iopub:{
        output:function(msg){
            var msg_type=msg.header.msg_type;
            var content = msg.content;
            if(msg_type==="stream"){
                callbacks.response = true;
                {{caller("content.text")}}
            }else if (msg_type==="display_data" || msg_type==="execute_result"){
                if (!!content.data["text/html"]){
                    {{caller('content.data["text/html"]')}}
                }
            }else if (msg_type === "error") {
                require(['base/js/utils'], function(utils) {
                    var tb = content.traceback;
                    if (tb && tb.length>0){
                        var data = tb.reduce(function(res, frame){return res+frame+'\\n';},"");
                        data = utils.fixConsole(data);
                        data = utils.fixCarriageReturn(data);
                        data = utils.autoLinkUrls(data);
                        $('#loading{{prefix}}').html("<pre>" + data +"</pre>");
                        callbacks.response = true;
                        {{caller({"message": 'content.evalue',"error": '"<pre>"+data+"</pre>"'})}}
                    }
                });
            }
            console.log("msg", msg);
        }
    }
}

!function(){
    $('#loading{{prefix}}').css('display','block');
    {%if command and (command|startswith("$$"))%}
    var command = {{command}};
    {%elif command%}
    var command= "{{command}}";
    {%endif%}
    {%if command%}
    function addOptions(options){
        function getStringRep(v) {
            if (!isNaN(parseFloat(v)) && isFinite(v)){
                return v.toString();
            }
            return "'" + v + "'";
        }
        for (var key in options){
            var value = options[key];
            var hasValue = value != null && typeof value !== 'undefined' && value !== '';
            var replaceValue = hasValue ? (key+"=" + getStringRep(value) ) : "";
            var pattern = (hasValue?"":",")+"\\s*" + key + "\\s*=\\s*'(\\\\'|[^'])*'";
            var rpattern=new RegExp(pattern);
            var n = command.search(rpattern);
            if ( n >= 0 ){
                command = command.replace(rpattern, replaceValue);
            }else if (hasValue){
                var n = command.lastIndexOf(")");
                command = [command.slice(0, n), (command[n-1]=="("? "":",") + replaceValue, command.slice(n)].join('')
            }        
        }
    }
    addOptions({{extraCommandOptions|oneline|trim}});
    {%endif%}
    if (typeof command == "undefined"){
        return alert("Unable to find command. Did you forget to define it?");
    }
    $('#' + {{targetId}}).html('<div style="width:100px;height:60px;left:47%;position:relative"><i class="fa fa-circle-o-notch fa-spin" style="font-size:48px"></i></div>'+
        '<div style="text-align:center">Loading your data. Please wait...</div>');

    console.log("Running command", command);
    IPython.notebook.session.kernel.execute(
        command, 
        callbacks, 
        {silent:true,store_history:false,stop_on_error:true}
    );
}()

{%- endmacro %}