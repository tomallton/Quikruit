The .json file (a .txt version is also available) in this zip contains a large JSON object consisting of 100,000 fake CVs for use in testing your system. The fields in each object are as follows:

Name --- The applicants name. For this project, assume this is enough for identification/contact purposes. 
Degree Qualification --- The type of degree the applicant has, i.e.: Computer Science, BSc
Degree level --- The level of degree awarded, i.e.: 1:1, 2:1
University Attended --- The University the applicant attended
A-Level Qualifications --- A list of JSON objects consisting of the subject title and the grade earned, i.e.: {"Subject": "Computing", "Grade": "A"}, {"Subject": "Mathematics", "Grade": "B"}, {"Subject": "Physics", "Grade": "C"}
Languages Known --- A list of programming languages the applicant knows. This is a list of JSON objects, consisting of the language name and skill at that language graded from 0-10, with 1 being little experience and 10 being an expert. i.e.: {"Language": "Java", "Expertise": 6}, {"Language": "Python", "Expertise": 8}, {"Language": "C++", "Expertise": 4}
Previous Employment --- A list of JSON objects detailing previous employment. This includes the institution/company, their position there and the length of time they worked there. i.e.:{"Company" : "Aperture Science", "Position" : "Software Developer", "Length of Employment": "1 year 6 months"}
Skills --- A list of skills outside of pure programming that the applicant may have, again with their expertise rated from 0-10. i.e.:{"Skill":"Excel","Expertise":4},{"Skill":"Public Speaking", "Expertise":7}
Hobbies --- A list of JSON objects detailing hobbies, includes a name and a level of interest rated from 1-10. 1 being barely interested, 10 being very interested. i.e.:{"Name":"Gaming", "Interest":5}, {"Name":"Reading", "Interest":8}, {"Name":"Fencing", "Interest":3}

