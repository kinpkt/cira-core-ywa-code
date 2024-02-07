var thaiParts = {Hand: 'มือ', Foot: 'เท้า', Butt: 'ก้น', Head: 'ศีรษะ', Knee: 'เข่า', Shoulder: 'ไหล่'}
var labelObj = payload.ywa_label;
label = '';

if (labelObj.no_parts.length > 0)
{
    var noPartsWarn = 'ตรวจไม่พบ: ';
    for (var i = 0; i < labelObj.no_parts.length; i++)
    {
        noPartsWarn += thaiParts[labelObj.no_parts[i]] + ' ';
    }
    label += noPartsWarn + '\n';
}
if (labelObj.pass_Knee_Foot && labelObj.pass_Shoulder_Hand && labelObj.pass_Shoulder_Knee)
{
    label = 'ท่าทางลักษณะถูกต้อง';
}
if (!labelObj.pass_Knee_Foot && labelObj.pass_Knee_Foot !== null)
{
    label += 'กรุณาปรับท่าช่วงไหล่-เท้า ตามเส้นสีเขียว\n';
}
    if (!labelObj.pass_Shoulder_Hand && labelObj.pass_Shoulder_Hand !== null)
{
    label += 'กรุณาปรับท่าช่วงไหล่-มือ ตามเส้นสีเขียว\n';
}
    if (!labelObj.pass_Shoulder_Knee && labelObj.pass_Shoulder_Knee !== null)
{
    label += 'กรุณาปรับท่าช่วงไหล่-เข่า ตามเส้นสีเขียว\n';
}