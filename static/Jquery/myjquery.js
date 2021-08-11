$(document).ready(function()
{
    jQuery.validator.addMethod("special",function(value, element){
        return /^[a-zA-Z]+$/.test(value);
    },"Please enter valid name");

   $('form[id="signupform"]').validate(
        {
           rules:{ fname:{required:true,special:true}   ,
                   lname:{required:true,special:true}   ,
                   email:{required:true,email:true} ,
                   pass1:{required:true,minlength:8},
                   pass2:{required:true,minlength:8}
                 },

           message:{
                       fname:"This Field is required" , 
                       lname:"This Field is required" , 
                       email:"This Field is required" ,
                       pass1:{minlength:"Password should be least 8 lenght"} 
           },

           submitHandler:function(form)
           {
               form.submit();
           }
       }
   )
});