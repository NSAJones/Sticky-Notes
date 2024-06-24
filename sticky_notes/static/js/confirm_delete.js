function confirmSubmit()
{
var agree=confirm(`This will delete your account and 
    all of your boards, continue?`);
if (agree)
 return true ;
else
 return false ;
}