<?php

class class_email_sender{

	private $name; 
	private $from;
	private $to;
	private $to_email;
	private $subject;
	private $headers;
	private $mail_message;

	public function __construct($name,$from,$to_email,$mail_message){

		$this->name=$name;
		$this->from=$from;
		$this->to_email=$to_email;
		$this->mail_message=$mail_message;

	}


	public function send_email(){


		$this->to=$this->to_email;
		//$this->headers="From : $this->from<$this->from>";

         $this->headers = 'From:'.$this->from. "\r\n" .
		'Reply-To: webmaster@example.com' . "\r\n" .
		'X-Mailer: PHP/' . phpversion();

		$this->subject="Query";
		$this->message="Name :" .$this->name. "\n";
		$this->message.="Email :" .$this->from."\n\n";
		$this->message.=$this->mail_message."\n\n";
		mail($this->to_email,$this->subject,$this->message,$this->headers);
		
		echo '<script>alert("Thanks for your mail.We will notify you shortly")</script>';

	}




//Class Finishes here	
}


?>
