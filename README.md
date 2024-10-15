# Image_Download_and_OCR
Pair of programs that download attachments from an email address and run OCR to extract the text from the downloaded image.

<h3>dl_email_attach.py</h3>
<p>Program downloads email attachments from a specified gmail account from today. Attachments are saved to a folder with today's date. If there if more than one attachment, the file name is incremented for each additional file.</p>

<p>In order to access a gmail account using this program, "Less Secure Apps" must be enabled for the gmail account. More information on this process can be found here: https://myaccount.google.com/lesssecureapps</p>

<p>After enabling less secure apps, a password can be generated by google (different from your gmail login password) that can be used in your program to access gmail.</p>

<p>IMAP is used to fetch attachments from gmail without the need for an email client. I used IMAP version 4rev1 described here: https://www.rfc-editor.org/rfc/rfc3501.</p>

<h3>ingredients_im2text.py</h3>
<p>Program takes image files from a directory and reads the image data into an openCV matrix. Binary thresholding is performed on the matrix such that any data value (corresponding to a pixel) below a certain value will be set to the minimum pixel color value (zero, black). All matrix data values above the threshold will be set to the maximum value (255 (white) for 8-bit numbers). This process makes the foreground text stand out from the background.</p>

<p>Next, the data values in the image matrix are dilated using a 3x3 kernel object to remove unnecessary artifacts and make the foreground text clearer. With the data operations complete, a bounding rectangle is placed around the image data to highlight the area we want to feed to OCR. After feeding the the image data to OCR, the recognized text is written to a file.</p>



