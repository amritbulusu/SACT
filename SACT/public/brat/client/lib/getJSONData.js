$(document).ready(function(){
var entities=[];
var docData={};
function testAjax() {
	var  i=0;
	var text=$(".getTextForAjax").val();
	var analyzeSyntax={
  "document": {
    "type": "PLAIN_TEXT",
    "content": text
  },
  "encodingType": "UTF8"
};

var bratURL='https://language.googleapis.com/v1/documents:analyzeSyntax?key=AIzaSyCbgqfDbTjaAVz-TA9XKrd-tlcpFTm4SVo';
  $.ajax({
    url:bratURL,
    data:JSON.stringify(analyzeSyntax),
    contentType: "application/json",
	dataType: "json",
    type:'post',
    cache:false,  
    success:function(data) {
    myData=data;
    console.log(data);
    for(j=0;j<myData.sentences.length;j++)
    {
    while (i < myData.tokens.length && i<myData.tokens[i].text.beginOffset<=(myData.tokens[i].text.beginOffset+myData.tokens[i].text.content.length-1)) { 
    	var start=myData.tokens[i].text.beginOffset;
    	var end=start+myData.tokens[i].text.content.length-1;
  entities.push([myData.tokens[i].text.content,myData.tokens[i].partOfSpeech.tag,
   [[start,end]]]);
  i=i+1;
};
}
console.log(entities);
var docData = {
    // Our text of choice
    text : text,
    // The entities entry holds all entity annotations
    entities : entities,
};
console.log(docData.entities);
 
    },
    error:function(){
		         
	}
  });
  
  }
  $(".getJson").click(function(){
testAjax();
		     });

	
})



