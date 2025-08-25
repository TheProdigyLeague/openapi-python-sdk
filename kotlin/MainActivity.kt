import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.wear.compose.foundation.weight
import com.example.jobportal.ui.theme.JobPortalTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            JobPortalTheme {
                JobApplicationScreen()
            }
        }
    }
}

@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)
@androidx.compose.runtime.Composable
fun JobApplicationScreen() {
    var fullName by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf("") }
    var phoneNumber by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf("") }
    var email by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf("") }
    var experience by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf("") }
    // In a real app, you'd have a way to handle resume file picking
    var resumeUri by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf<android.net.Uri?>(null) }


    androidx.compose.material3.Scaffold(
        topBar = {
            androidx.compose.material3.CenterAlignedTopAppBar(
                title = { androidx.compose.material3.Text(stringResource(R.string.job_application_portal)) } // "职位申请门户"
            )
        }
    ) { paddingValues ->
        androidx.compose.foundation.layout.Column(
            modifier = Modifier
                .padding(paddingValues)
                .padding(16.dp)
                .verticalScroll(rememberScrollState()) // Makes the column scrollable
                .fillMaxSize(),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = androidx.compose.foundation.layout.Arrangement.spacedBy(12.dp)
        ) {

            androidx.compose.material3.Text(
                text = stringResource(R.string.personal_information_header), // "个人信息"
                style = androidx.compose.material3.MaterialTheme.typography.titleMedium
            )

            androidx.compose.material3.OutlinedTextField(
                value = fullName,
                onValueChange = { fullName = it },
                label = { androidx.compose.material3.Text(stringResource(R.string.label_full_name)) }, // "全名"
                modifier = Modifier.fillMaxWidth(),
                singleLine = true,
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Next)
            )

            androidx.compose.material3.OutlinedTextField(
                value = phoneNumber,
                onValueChange = { phoneNumber = it },
                label = { androidx.compose.material3.Text(stringResource(R.string.label_phone_number)) }, // "电话号码"
                modifier = Modifier.fillMaxWidth(),
                keyboardOptions = KeyboardOptions(
                    keyboardType = KeyboardType.Phone,
                    imeAction = ImeAction.Next
                ),
                singleLine = true
            )

            androidx.compose.material3.OutlinedTextField(
                value = email,
                onValueChange = { email = it },
                label = { androidx.compose.material3.Text(stringResource(R.string.label_email)) }, // "电子邮件"
                modifier = Modifier.fillMaxWidth(),
                keyboardOptions = KeyboardOptions(
                    keyboardType = KeyboardType.Email,
                    imeAction = ImeAction.Next
                ),
                singleLine = true
            )

            androidx.compose.foundation.layout.Spacer(modifier = Modifier.height(16.dp))

            androidx.compose.material3.Text(
                text = stringResource(R.string.work_experience_header), // "工作经验和简历"
                style = androidx.compose.material3.MaterialTheme.typography.titleMedium
            )

            androidx.compose.material3.OutlinedTextField(
                value = experience,
                onValueChange = { experience = it },
                label = { androidx.compose.material3.Text(stringResource(R.string.label_work_experience)) }, // "相关工作经验 (简述)"
                modifier = Modifier.fillMaxWidth().height(120.dp),
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Done)
            )

            // Resume Upload Placeholder
            androidx.compose.material3.Button(
                onClick = {
                    // In a real app, this would trigger a file picker
                    // For now, it's just a placeholder action
                    println("Upload Resume Clicked. URI: $resumeUri")
                },
                modifier = Modifier.fillMaxWidth()
            ) {
                // You would show the selected file name if resumeUri is not null
                androidx.compose.material3.Text(
                    if (resumeUri == null) stringResource(R.string.button_upload_resume) // "上传简历"
                    else stringResource(R.string.button_resume_selected) // "简历已选择"
                )
            }
            if (resumeUri != null) {
                androidx.compose.material3.Text(
                    text = "Selected file: ${resumeUri?.lastPathSegment}", // Example of showing file name
                    style = androidx.compose.material3.MaterialTheme.typography.bodySmall
                )
            }


            androidx.compose.foundation.layout.Spacer(modifier = Modifier.weight(1.0f)) // Pushes button to bottom if content is short

            androidx.compose.material3.Button(
                onClick = {
                    // Handle submission logic
                    println("Submit Clicked: $fullName, $phoneNumber, $email, $experience")
                },
                modifier = Modifier.fillMaxWidth(),
                enabled = fullName.isNotBlank() && phoneNumber.isNotBlank() && email.isNotBlank() // Basic validation
            ) {
                androidx.compose.material3.Text(stringResource(R.string.button_submit_application)) // "提交申请"
            }
        }
    }
}

// You would define these in your strings.xml
/*
<resources>
    <string name="app_name">JobPortal</string>
    <string name="job_application_portal">职位申请门户</string>
    <string name="personal_information_header">个人信息</string>
    <string name="label_full_name">全名 (Xìngmíng)</string>
    <string name="label_phone_number">电话号码 (Diànhuà hàomǎ)</string>
    <string name="label_email">电子邮件 (Diànzǐ yóujiàn)</string>
    <string name="work_experience_header">工作经验和简历</string>
    <string name="label_work_experience">相关工作经验 (简述)</string>
    <string name="button_upload_resume">上传简历 (Shàngchuán jiǎnlì)</string>
    <string name="button_resume_selected">简历已选择</string>
    <string name="button_submit_application">提交申请 (Tíjiāo shēnqǐng)</string>
</resources>
*/

@Preview(showBackground = true, locale = "zh-rCN") // Preview with Chinese locale
@Preview(showBackground = true)
@androidx.compose.runtime.Composable
fun DefaultPreview() {
    JobPortalTheme {
        JobApplicationScreen()
    }
}