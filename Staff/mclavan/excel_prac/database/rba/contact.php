<?php 
error_reporting(E_ALL ^ E_NOTICE); // hide all basic notices from PHP

//If the form is submitted
if(isset($_POST['submitted'])) {
	
	// require a name from user
	if(trim($_POST['firstName']) === '') {
		$firstNameError =  'Forgot your First name!'; 
		$hasError = true;
	} else {
		$firstName = trim($_POST['firstName']);
	}
	
	if(trim($_POST['lastName']) === '') {
		$lastNameError =  'Forgot your Last name!'; 
		$hasError = true;
	} else {
		$lastName = trim($_POST['lastName']);
	}
	
	if(trim($_POST['imName']) === '') {
		$imNameError =  'Forgot your Ichat ID!'; 
		$hasError = true;
	} else {
		$imName = trim($_POST['imName']);
	}
	
	
	if(trim($_POST['studentNumber']) === '') {
		$studentNumberError =  'Forgot your Last name!'; 
		$hasError = true;
	} else {
		$studentNumber = trim($_POST['studentNumber']);
	}
	
	if($_POST['carreerPath'] === NULL) {
		$carreerPathError =  'Forgot your carreer path!'; 
		$hasError = true;
	} else {
		$carreerPath = ($_POST['carreerPath']);
	}
		if($_POST['technical'] === NULL) {
		$technicalError =  'Forgot to tell me if you are technical!'; 
		$hasError = true;
	} else {
		$technical = ($_POST['technical']);
	}
	
	if(trim($_POST['classNumber']) === '') {
		$classNumberError =  'Forgot your Class number!'; 
		$hasError = true;
	} else {
		$classNumber = trim($_POST['classNumber']);
	}
	// need valid email
	if(trim($_POST['email']) === '')  {
		$emailError = 'Forgot to enter in your e-mail address.';
		$hasError = true;
	} else if (!preg_match("/^[[:alnum:]][a-z0-9_.-]*@[a-z0-9.-]+\.[a-z]{2,4}$/i", trim($_POST['email']))) {
		$emailError = 'You entered an invalid email address.';
		$hasError = true;
	} else {
		$email = trim($_POST['email']);
	}
	
	
	// upon no failure errors let's email now!
	if(!isset($hasError)) {
		include 'Loginfo.php';
		$query = "INSERT INTO Student_info VALUES('', '$firstName' ,'$lastName', '$studentNumber', '$classNumber', '$imName', '$email', '$carreerPath', '$technical', NOW() )";
		
		mysql_query($query, $link) or die("Unable to select: ".mysql_error());
        // set our boolean completion value to TRUE
		$formSent = true;
		
		mysql_close($link);
	}
}
?>
<!DOCTYPE html>
<head> 
<title>RBA Contact Form</title>
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.js"></script>
<script src="http://cdn.jquerytools.org/1.2.5/full/jquery.tools.min.js"></script>
<script src="jquery.easing.1.3.js"></script>


<link href="styles.css" rel="stylesheet" type="text/css" />
</head>

<body>
    <!-- @begin contact -->
    <div id="setup">
	<div id="contact" class="section">
		<div class="container content">
		
	        <?php if(isset($formSent) && $formSent == true) { ?>
                <p class="info">Form Sent.</p>
            <?php } else { ?>
            
				<div class="desc">
					<h2>Contact Information</h2>
					
					<p class="desc">Please use the contact form below so that we have a way to contact you.</p>
				</div>
				
				<div id="contact-form">
					<?php if(isset($hasError) || isset($captchaError) ) { ?>
                        <p class="alert">Error submitting the form</p>
                    <?php } ?>
				
					<form id="contact-information" action="contact.php" method="post" action="#">
						<div class="formblock">

                            <label class="screen-reader-text">First Name</label>
                            <input type="text" name="firstName" id="firstName" value="<?php if(isset($_POST['firstName'])) echo $_POST['firstName'];?>" class="txt requiredField" placeholder="First Name:" title="Please enter your first name." />
                            <?php if($firstNameError != '') { ?>
                                <br /><span class="error"><?php echo $firstNameError;?></span> 
                            <?php } ?>

						</div>
                        
						<div class="formblock">

                            <label class="screen-reader-text">Last Name</label>
                            <input type="text" name="lastName" id="lastName" value="<?php if(isset($_POST['lastName'])) echo $_POST['lastName'];?>" class="txt requiredField" placeholder="Last Name:" title="Please enter your last name." />
                            <?php if($lastNameError != '') { ?>
                                <br /><span class="error"><?php echo $lastNameError;?></span> 
                            <?php } ?>

						</div>
                        
						<div class="formblock">

                            <label class="screen-reader-text">Student Number</label>
                            <input type="text" name="studentNumber" id="studentNumber" value="<?php if(isset($_POST['studentNumber'])) echo $_POST['studentNumber'];?>" class="txt requiredField" placeholder="Student Number:" title="Please enter your student number." />
                            <?php if($studentNumberError != '') { ?>
                                <br /><span class="error"><?php echo $studentNumberError;?></span> 
                            <?php } ?>

						</div>
                        
						<div class="formblock">

                            <label class="screen-reader-text">Ichat Name</label>
                            <input type="text" name="imName" id="imName" value="<?php if(isset($_POST['imName'])) echo $_POST['imName'];?>" class="txt requiredField" placeholder="IChat Name:" title="Please enter your ichat name, or enter none if you don't have one." />
                            <?php if($imNameError != '') { ?>
                                <br /><span class="error"><?php echo $imNameError;?></span> 
                            <?php } ?>

						</div>
                        
                        
                        
						<div class="formblock">

                            <label class="screen-reader-text">Email</label>
                            <input type="text" name="email" id="email" value="<?php if(isset($_POST['email']))  echo $_POST['email'];?>" class="txt requiredField email" placeholder="Email:" title="Please enter the best email address to contact you with." />
                            <?php if($emailError != '') { ?>
                                <br /><span class="error"><?php echo $emailError;?></span>
                            <?php } ?>

						</div>
                        
                        
						<div class="formblock">

                            <label class="screen-reader-text">Class number</label>
                            <input type="text" name="classNumber" id="classNumber" value="<?php if(isset($_POST['classNumber'])) echo $_POST['classNumber'];?>" class="txt requiredField" placeholder="Class number:" title="Year followed by month, no slashes, dashes or spaces." />
                            <?php if($classNumberError != '') { ?>
                                <br /><span class="error"><?php echo $classNumberError;?></span> 
                            <?php } ?>

						</div>
                        
                                                
                        <div class="formblock">

                            <label class="screen-reader-text">Carreer Path</label>
                            <input type="radio" name="carreerPath" id="cm" value="Character Modeling" class="radioButton" />Character Modeling <br />
                            <input type="radio" name="carreerPath" id="em" value="Environment Modeling" class="radioButton"/>Environment Modeling <br />
                            <input type="radio" name="carreerPath" id="comp" value="Compositing" class="radioButton" />Compositing<br />
                            <input type="radio" name="carreerPath" id="vef" value="Visual Effects" class="radioButton" />Visual Effects <br />
                            <input type="radio" name="carreerPath" id="sal" value="Shading and Lighting" class="radioButton" />Shading and Lighting<br />
                            <input type="radio" name="carreerPath" id="anim" value="Animation" class="radioButton" />Animation<br />
                            <input type="radio" name="carreerPath" id="rig" value="Rigging" class="radioButton"  />Rigging <br />
                            <input type="radio" name="carreerPath" id="other" value="Other" class="radioButton"  />Other <br />
                            
                            <?php if($carreerPathError != '') { ?>
                                <br /><span class="error"><?php echo $carreerPathError;?></span>
                            <?php } ?>

						</div>
                                           
                        <div class="formblock">

                            <label class="screen-reader-text" title=" - Some artists are very technical and can build their own tools and scripts. Are you interested in some advanced tasks to help improve your technical abilities?">Are you a technical artist?</label>
                            <input type="radio" name="technical" id="techYes" value=1 class="radioButton" title="You have some experience with scripting or programming or would like to explore advanced topics in scripting. - Some artists are very technical and can build their own tools and scripts." />Yes<br />
                            <input type="radio" name="technical" id="techNo" value=0 class="radioButton" title="You have no interest in advanced topics in scripting - Some artists are very technical and can build their own tools and scripts." />No<br />
                            <?php if($technicalError != '') { ?>
                                <br /><span class="error"><?php echo $technicalError;?></span>
                            <?php } ?>

						</div>
                        <div class="submit">
							<button name="submit" type="submit" class="subbutton">Submit</button>
							<input type="hidden" name="submitted" id="submitted" value="true" />
                        </div>
					</form>			
				</div>
				
			<?php } ?>
		</div>
    </div>
    </div><!-- End #contact -->
	
<script type="text/javascript">
	<!--//--><![CDATA[//><!--
	$(document).ready(function() {
		$('form#contact-information').submit(function() {
			$('form#contact-information .error').remove();
			var hasError = false;
			$('.requiredField').each(function() {
				if($.trim($(this).val()) == '') {
					var labelText = $(this).prev('label').text();
					$(this).parent().append('<span class="error">You forgot to enter your '+labelText+'.</span>');
					$(this).addClass('inputError');
					hasError = true; 
				} else if($(this).hasClass('email')) {
					var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
					if(!emailReg.test($.trim($(this).val()))) {
						var labelText = $(this).prev('label').text();
						$(this).parent().append('<span class="error">Sorry! You\'ve entered an invalid '+labelText+'.</span>');
						$(this).addClass('inputError');
						hasError = true;
					}
				}
			});
			
			if($('input[name=carreerPath]:checked').val() == null){
				$('input[name=carreerPath]').parent().append(' <span class="error">Sorry! You need to tell me what carreer path you think you\'ll take. </span>');
				hasError = true;
			}
			if($('input[name=technical]:checked').val() == null){
				$('input[name=technical]').parent().append(' <span class="error">Sorry! You need to tell me if you think you\'re a technical person. </span>');
				hasError = true;
			}
			
			if(!hasError) {
				var formInput = $(this).serialize();
				$.post($(this).attr('action'),formInput, function(data){
					var delayAmt = 500
					$('form#contact-information').slideUp(delayAmt, "easeOutBounce", function() {				   
						//$(this).before('<p class="tick"><strong>Thanks!</strong> Form Sent</p>');
					}).delay(delayAmt).before('<p class="tick"><strong>Thanks!</strong> Form Sent</p>'); 
					
				});
			}
			
			return false;	
		});
	});

	//-->!]]>
</script>

<script type="text/javascript">	
	<!--//--><![CDATA[//><!--
$(function() {
	$.tools.tooltip.addEffect("elastic",
	
		// opening animation
		function(done) {
			this.getTip().animate({top: '+=15'}, 500, 'easeOutElastic', done).show();
		},
	
		// closing animation
		function(done) {
			this.getTip().animate({top: '-=15'}, 500, 'easeInElastic', function()  {
				$(this).hide();
				done.call();
			});
		}
	);
	
	$("#contact-information :input[type=text]").tooltip({
		position: "center right",
		offset: [-10, 10],
		effect: "elastic",
	});
	
	$("#contact-information :input[name=technical]").tooltip({
		position: "center right",
		offset: [0, 10],
		delay: 0,
	});

});
	//-->!]]>
</script>

</body>
</html>