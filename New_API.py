# Core Pkgs
import streamlit as st
st. set_page_config(layout="wide")
from PyPDF2 import PdfReader
import re
# EDA Pkgs
import pandas as pd
import numpy as np
# Data Viz Pkg
import matplotlib.pyplot as plt
import matplotlib
import scipy
matplotlib.use("Agg")
import seaborn as sns



def main():
    """Semi Automated ML App with Streamlit """

    activities = ["EDA", "Plots"]
    choice = st.sidebar.selectbox("Select Activities", activities)
    st.set_option('deprecation.showPyplotGlobalUse', False)


    def BE1sem(data):
        name = []
        seat = []
        sgpa = []

        s410241 = []
        s410242 = []
        s410243 = []
        s410244 = []
        s410245 = []
        s410246 = []
        s410247 = []
        s410248 = []

        subject_name = ['410241 Design and Analysis of Algorithms',
                        '410242 Machine Learning',
                        '410243 Blockchain Technology',
                        '410244 Elective III',
                        '410245 Elective IV',
                        '410246: Laboratory Practice III',
                        '410247: Laboratory Practice IV',
                        '410248: Project Stage I']

        #Number_pages = int(input("Please Enter the Number of Pages:-"))
        Number_pages = int(st.number_input('Please Enter the Number of Pages:-'))

        if Number_pages is not None:
            reader = PdfReader(data)

            if reader is not None:
                for se in range(0, Number_pages):
                    page = reader.pages[se]
                    text = page.extract_text()
                    content = text.splitlines()

                    for i in content:
                        if ('SEAT ' in i):
                            # print(i[10:20])  # this is for Seat number
                            seat.append(i[10:20])
                            # print(i[28:63]) # this is for Name
                            name.append(i[28:63])
                        if ('SGPA' in i):
                            s = [float(s) for s in re.findall(r'-?\d+\.?\d*', i[5:])]
                            if (len(s) == 1):
                                sgpa.append(0)
                            elif (len(s) == 2):
                                sgpa.append(s[0])

                            # sgpa.append(i[8:12])
                        # elif ('SGPA1' in i):
                        #     sgpa.append(i[7:11])
                        if ('410241' in i):
                            s410241.append(i[97:101])
                        if ('410242' in i):
                            s410242.append(i[97:101])
                        if ('410243' in i):
                            s410243.append(i[97:101])
                        if ('410244' in i):
                            s410244.append(i[97:101])
                        if ('410245' in i):
                            s410245.append(i[97:101])
                        if ('410246' in i):
                            s410246.append(i[97:101])
                        if ('410247' in i):
                            s410247.append(i[97:101])
                        if ('410248' in i):
                            s410248.append(i[97:101])

                df = pd.DataFrame(columns=subject_name)
                df.insert(0, 'SEAT NO.', None, True)
                df.insert(1, 'Candidate Name', None, True)
                df['SEAT NO.'] = seat
                df['Candidate Name'] = name

                df['410241 Design and Analysis of Algorithms'] = s410241
                df['410242 Machine Learning'] = s410242
                df['410243 Blockchain Technology'] = s410243
                df['410244 Elective III'] = s410244
                df['410245 Elective IV'] = s410245
                df['410246: Laboratory Practice III'] = s410246
                df['410247: Laboratory Practice IV'] = s410247
                df['410248: Project Stage I'] = s410248
                df['SGPA'] = sgpa

                # df['SGPA'] = df['SGPA'].str.replace('--,', "")
                # df['SGPA'] = df['SGPA'].str.replace(',T', "")
                # df['SGPA'] = df['SGPA'].replace(r'^\s*$', np.nan, regex=True)
                df['SGPA'] = df['SGPA'].astype('float64')

                subjectName = list(df.columns.values)
                subjectName.remove('SEAT NO.')
                subjectName.remove('Candidate Name')
                subjectName.remove('SGPA')
                listsub = []
                listno = []
                listper = []

                for ij in subjectName:
                    df[ij] = df[ij].str.replace("FF", "")
                    df[ij] = df[ij].replace(r'^\s*$', np.nan, regex=True)
                    df[ij] = df[ij].astype('float64')

                df = df.fillna(0)

                st.subheader("TOP 5 Students")
                top5 = df.nlargest(5, 'SGPA')
                top5.index = np.arange(1, len(top5) + 1)
                top5[['SEAT NO.', 'Candidate Name', 'SGPA']]

                for sub in subjectName:
                    count = 0
                    percentage = 0
                    for i in df[sub]:
                        if (i < 40):
                            count += 1
                    percentage = round(((count / len(df[sub])) * 100), 2)
                    listsub.append(sub)
                    listno.append(count)
                    listper.append(percentage)
                Display = pd.DataFrame({'Subject': listsub, 'Number of Student': listno, 'Percentage %': listper})
                Display.index = np.arange(1, len(Display) + 1)
                pd.set_option('display.colheader_justify', 'center')
                st.subheader("Subject Wise Failure Percentage")
                # st.dataframe(Display, width=500, height=560)
                Display

                Total_no_student = len(df['SGPA'])
                marks_classes = ['Appeared', 'Distinction', 'First Class', 'Higher Second Class', 'Seconde Class',
                                 'Pass Class',
                                 'No. of student Pass', 'Fail', '% of Pass', '% of Fail']
                First_Class_with_Distiction = 0
                First_Class = 0
                Higher_Seconde_Class = 0
                Second_Class = 0
                Pass_Class = 0
                fclass = 0
                for i in df['SGPA']:
                    if (i >= 7.75):
                        First_Class_with_Distiction += 1
                    elif (i >= 6.75 and i < 7.75):
                        First_Class += 1
                    elif (i >= 6.25 and i < 6.75):
                        Higher_Seconde_Class += 1
                    elif (i >= 5.5 and i < 6.25):
                        Second_Class += 1
                    elif (i > 4.65 and i < 5.5):
                        Pass_Class += 1
                    elif (i < 4.65):
                        fclass += 1
                Full_pass = First_Class_with_Distiction + First_Class + Higher_Seconde_Class + Second_Class + Pass_Class
                pass_percentage = float(Full_pass / Total_no_student) * 100
                fail_percentage = float(fclass / Total_no_student) * 100
                df1 = pd.DataFrame(columns=marks_classes, index=[1])
                df1['Appeared'] = Total_no_student
                df1['Distinction'] = First_Class_with_Distiction
                df1['First Class'] = First_Class
                df1['Higher Second Class'] = Higher_Seconde_Class
                df1['Seconde Class'] = Second_Class
                df1['Pass Class'] = Pass_Class
                df1['No. of student Pass'] = Full_pass
                df1['Fail'] = fclass
                df1['% of Pass'] = pass_percentage
                df1['% of Fail'] = fail_percentage

                st.write(df1)

                if st.checkbox("Do you Want to Download Excel File"):
                    sheet_name = st.text_input("Enter Sheet Name")
                    if sheet_name is not None:
                        df.index = np.arange(1, len(df) + 1)
                        df.to_excel("BE First Semester.xlsx", sheet_name=sheet_name)

                return df






    def TE1sem(data):
        name = []
        seat = []
        sgpa = []

        s310241 = []
        s310242 = []
        s310243 = []
        s310244 = []
        s310245 = []
        s310246 = []
        s310247 = []
        s310248 = []
        s310249 = []

        subject_name = ['310241 Database Management Systems',
                        '310242 Theory of Computation',
                        '310243 Systems Programming and Operating System',
                        '310244 Computer Networks and Security',
                        '310245 Elective I',
                        '310246 Database Management Systems Laboratory',
                        '310247 Computer Networks and Security Laboratory',
                        '310248 Laboratory Practice I',
                        '310249 Seminar and Technical Communication']

        #Number_pages = int(input("Please Enter the Number of Pages:-"))
        Number_pages = int(st.number_input('Please Enter the Number of Pages:-'))

        if Number_pages is not None:
            reader = PdfReader(data)
            if reader is not None:
                for te in range(0, Number_pages):
                    page = reader.pages[te]
                    text = page.extract_text()
                    content = text.splitlines()

                    for i in content:
                        if ('SEAT ' in i):
                            # print(i[10:20])  # this is for Seat number
                            seat.append(i[10:20])
                            # print(i[28:63]) # this is for Name
                            name.append(i[28:63])
                        if ('SGPA' in i):
                            s = [float(s) for s in re.findall(r'-?\d+\.?\d*', i[5:])]
                            if (len(s) == 1):
                                sgpa.append(0)
                            elif (len(s) == 2):
                                sgpa.append(s[0])
                            # sgpa.append(i[8:12])

                        # elif ('SGPA1' in i):
                        #     sgpa.append(i[7:11])
                        if ('310241' in i):
                            s310241.append(i[97:101])
                        if ('310242' in i):
                            s310242.append(i[97:101])
                        if ('310243' in i):
                            s310243.append(i[97:101])
                        if ('310244' in i):
                            s310244.append(i[97:101])
                        if ('310245' in i):
                            s310245.append(i[97:101])
                        if ('310246' in i):
                            s310246.append(i[97:101])
                        if ('310247' in i):
                            s310247.append(i[97:101])
                        if ('310248' in i):
                            s310248.append(i[97:101])
                        if ('310249' in i):
                            s310249.append(i[97:101])

                df = pd.DataFrame(columns=subject_name)
                df.insert(0, 'SEAT NO.', None, True)
                df.insert(1, 'Candidate Name', None, True)
                df['SEAT NO.'] = seat
                df['Candidate Name'] = name
                df['310241 Database Management Systems'] = s310241
                df['310242 Theory of Computation'] = s310242
                df['310243 Systems Programming and Operating System'] = s310243
                df['310244 Computer Networks and Security'] = s310244
                df['310245 Elective I'] = s310245
                df['310246 Database Management Systems Laboratory'] = s310246
                df['310247 Computer Networks and Security Laboratory'] = s310247
                df['310248 Laboratory Practice I'] = s310248
                df['310249 Seminar and Technical Communication'] = s310249
                df['SGPA'] = sgpa

                # df['SGPA'] = df['SGPA'].str.replace('--,', "")
                # df['SGPA'] = df['SGPA'].str.replace(',T', "")
                # df['SGPA'] = df['SGPA'].replace(r'^\s*$', np.nan, regex=True)
                df['SGPA'] = df['SGPA'].astype('float64')

                subjectName = list(df.columns.values)
                subjectName.remove('SEAT NO.')
                subjectName.remove('Candidate Name')
                subjectName.remove('SGPA')
                listsub = []
                listno = []
                listper = []

                for ij in subjectName:
                    df[ij] = df[ij].str.replace("FF", "")
                    df[ij] = df[ij].replace(r'^\s*$', np.nan, regex=True)
                    df[ij] = df[ij].astype('float64')

                df = df.fillna(0)

                st.subheader("TOP 5 Students")
                top5 = df.nlargest(5, 'SGPA')
                top5.index = np.arange(1, len(top5) + 1)
                top5[['SEAT NO.', 'Candidate Name', 'SGPA']]

                for sub in subjectName:
                    count = 0
                    percentage = 0
                    for i in df[sub]:
                        if (i < 40):
                            count += 1
                    percentage = round(((count / len(df[sub])) * 100), 2)
                    listsub.append(sub)
                    listno.append(count)
                    listper.append(percentage)
                Display = pd.DataFrame({'Subject': listsub, 'Number of Student': listno, 'Percentage %': listper})
                Display.index = np.arange(1, len(Display) + 1)
                pd.set_option('display.colheader_justify', 'center')
                st.subheader("Subject Wise Failure Percentage")
                # st.dataframe(Display,width=500,height=560)
                Display

                Total_no_student = len(df['SGPA'])
                marks_classes = ['Appeared', 'Distinction', 'First Class', 'Higher Second Class', 'Seconde Class',
                                 'Pass Class',
                                 'No. of student Pass', 'Fail', '% of Pass', '% of Fail']
                First_Class_with_Distiction = 0
                First_Class = 0
                Higher_Seconde_Class = 0
                Second_Class = 0
                Pass_Class = 0
                fclass = 0
                for i in df['SGPA']:
                    if (i >= 7.75):
                        First_Class_with_Distiction += 1
                    elif (i >= 6.75 and i < 7.75):
                        First_Class += 1
                    elif (i >= 6.25 and i < 6.75):
                        Higher_Seconde_Class += 1
                    elif (i >= 5.5 and i < 6.25):
                        Second_Class += 1
                    elif (i > 4.65 and i < 5.5):
                        Pass_Class += 1
                    elif (i < 4.65):
                        fclass += 1
                Full_pass = First_Class_with_Distiction + First_Class + Higher_Seconde_Class + Second_Class + Pass_Class
                pass_percentage = float(Full_pass / Total_no_student) * 100
                fail_percentage = float(fclass / Total_no_student) * 100
                df1 = pd.DataFrame(columns=marks_classes, index=[1])
                df1['Appeared'] = Total_no_student
                df1['Distinction'] = First_Class_with_Distiction
                df1['First Class'] = First_Class
                df1['Higher Second Class'] = Higher_Seconde_Class
                df1['Seconde Class'] = Second_Class
                df1['Pass Class'] = Pass_Class
                df1['No. of student Pass'] = Full_pass
                df1['Fail'] = fclass
                df1['% of Pass'] = pass_percentage
                df1['% of Fail'] = fail_percentage

                st.write(df1)

                if st.checkbox("Do you Want to Download Excel File"):
                    sheet_name = st.text_input("Enter Sheet Name")
                    if sheet_name is not None:
                        df.index = np.arange(1, len(df) + 1)
                        df.to_excel("TE First Semester.xlsx", sheet_name=sheet_name)

                return df



    def SE1sem(data):
        name = []
        seat = []
        sgpa = []

        s210241 = []
        s210242 = []
        s210243 = []
        s210244 = []
        s210245 = []
        s210246 = []
        s210247 = []
        s210248 = []
        s210249 = []
        s210250 = []

        subject_name = ['210241 Discrete Mathematics',
                        '210242 Fundamentals of Data Structures',
                        '210243 Object Oriented Programming (OOP)',
                        '210244 Computer Graphics',
                        '210245 Digital Electronics and Logic Design',
                        '210246 Data Structures Laboratory',
                        '210247 OOP and Computer Graphics Laboratory',
                        '210248 Digital Electronics Laboratory',
                        '210249 Business Communication Skills',
                        '210250 Humanity and Social Science']

        #Number_pages = int(input("Please Enter the Number of Pages:-"))
        Number_pages = int(st.number_input('Please Enter the Number of Pages:-'))

        if Number_pages is not None:
            reader = PdfReader(data)
            if reader is not None:
                for se in range(0, Number_pages):
                    page = reader.pages[se]
                    text = page.extract_text()
                    content = text.splitlines()

                    for i in content:
                        if ('SEAT' in i):
                            # print(i[10:20])  # this is for Seat number
                            seat.append(i[10:20])
                            # print(i[28:63]) # this is for Name
                            name.append(i[28:63])
                            # print(i)
                        if ('SGPA' in i):
                            # print(i[8:12])
                            s = [float(s) for s in re.findall(r'-?\d+\.?\d*', i[5:])]
                            if (len(s) == 1):
                                sgpa.append(0)
                            elif (len(s) == 2):
                                sgpa.append(s[0])
                            # sgpa.append(i[8:12])

                            # print(i)
                        # elif ('SGPA1' in i):
                        #     x=(re.findall("\d+\.\d+",i))
                        #     sgpa.extend(x)
                        if ('210241' in i):
                            s210241.append(i[97:101])
                        if ('210242' in i):
                            s210242.append(i[97:101])
                        if ('210243' in i):
                            s210243.append(i[97:101])
                        if ('210244' in i):
                            s210244.append(i[97:101])
                        if ('210245' in i):
                            s210245.append(i[97:101])
                        if ('210246' in i):
                            s210246.append(i[97:101])
                        if ('210247' in i):
                            s210247.append(i[97:101])
                        if ('210248' in i):
                            s210248.append(i[97:101])
                        if ('210249' in i):
                            s210249.append(i[97:101])
                        if ('210250' in i):
                            s210250.append(i[97:101])

                df = pd.DataFrame(columns=subject_name)
                df.index = np.arange(1, len(df) + 1)
                df.insert(0, 'SEAT NO.', None, True)
                df.insert(1, 'Candidate Name', None, True)
                df['SEAT NO.'] = seat
                df['Candidate Name'] = name

                df['210241 Discrete Mathematics'] = s210241
                df['210242 Fundamentals of Data Structures'] = s210242
                df['210243 Object Oriented Programming (OOP)'] = s210243
                df['210244 Computer Graphics'] = s210244
                df['210245 Digital Electronics and Logic Design'] = s210245
                df['210246 Data Structures Laboratory'] = s210246
                df['210247 OOP and Computer Graphics Laboratory'] = s210247
                df['210248 Digital Electronics Laboratory'] = s210248
                df['210249 Business Communication Skills'] = s210249
                df['210250 Humanity and Social Science'] = s210250
                df['SGPA'] = sgpa

                seat.clear()
                name.clear()
                s210241.clear()
                s210242.clear()
                s210243.clear()
                s210244.clear()
                s210245.clear()
                s210246.clear()
                s210247.clear()
                s210248.clear()
                s210249.clear()
                s210250.clear()
                sgpa.clear()

                # df['SGPA'] = df['SGPA'].str.replace('--,', "")
                # df['SGPA'] = df['SGPA'].str.replace('-,', "")
                # df['SGPA'] = df['SGPA'].str.replace(',T', "")
                # df['SGPA'] = df['SGPA'].str.replace('T', "")
                # df['SGPA'] = df['SGPA'].str.replace(',', "")
                # df['SGPA'] = df['SGPA'].str.replace('EAR', "")
                # df['SGPA'] = df['SGPA'].str.replace(', T', "")
                # df['SGPA'] = df['SGPA'].replace(r'^\s*$', np.nan, regex=True)
                df['SGPA'] = df['SGPA'].astype('float64')

                subjectName = list(df.columns.values)
                subjectName.remove('SEAT NO.')
                subjectName.remove('Candidate Name')
                subjectName.remove('SGPA')
                listsub = []
                listno = []
                listper = []

                for ij in subjectName:
                    df[ij] = df[ij].str.replace("FF", "")
                    df[ij] = df[ij].replace(r'^\s*$', np.nan, regex=True)
                    df[ij] = df[ij].astype('float64')

                df = df.fillna(0)

                st.subheader("TOP 5 Students")
                top5 = df.nlargest(5, 'SGPA')
                top5.index = np.arange(1, len(top5) + 1)
                top5[['SEAT NO.', 'Candidate Name', 'SGPA']]

                for sub in subjectName:
                    count = 0
                    percentage = 0
                    for i in df[sub]:
                        if (i < 40):
                            count += 1
                    percentage = round(((count / len(df[sub])) * 100), 2)
                    listsub.append(sub)
                    listno.append(count)
                    listper.append(percentage)
                Display = pd.DataFrame({'Subject': listsub, 'Number of Student': listno, 'Percentage %': listper})
                Display.index = np.arange(1, len(Display) + 1)
                pd.set_option('display.colheader_justify', 'center')
                st.subheader("Subject Wise Failure Percentage")
                # st.dataframe(Display, width=500, height=560)
                Display

                Total_no_student = len(df['SGPA'])
                marks_classes = ['Appeared', 'Distinction', 'First Class', 'Higher Second Class', 'Seconde Class',
                                 'Pass Class',
                                 'No. of student Pass', 'Fail', '% of Pass', '% of Fail']
                First_Class_with_Distiction = 0
                First_Class = 0
                Higher_Seconde_Class = 0
                Second_Class = 0
                Pass_Class = 0
                fclass = 0
                for i in df['SGPA']:
                    if (i >= 7.75):
                        First_Class_with_Distiction += 1
                    elif (i >= 6.75 and i < 7.75):
                        First_Class += 1
                    elif (i >= 6.25 and i < 6.75):
                        Higher_Seconde_Class += 1
                    elif (i >= 5.5 and i < 6.25):
                        Second_Class += 1
                    elif (i > 4.65 and i < 5.5):
                        Pass_Class += 1
                    elif (i < 4.65):
                        fclass += 1
                Full_pass = First_Class_with_Distiction + First_Class + Higher_Seconde_Class + Second_Class + Pass_Class
                pass_percentage = float(Full_pass / Total_no_student) * 100
                fail_percentage = float(fclass / Total_no_student) * 100
                df1 = pd.DataFrame(columns=marks_classes, index=[1])
                df1['Appeared'] = Total_no_student
                df1['Distinction'] = First_Class_with_Distiction
                df1['First Class'] = First_Class
                df1['Higher Second Class'] = Higher_Seconde_Class
                df1['Seconde Class'] = Second_Class
                df1['Pass Class'] = Pass_Class
                df1['No. of student Pass'] = Full_pass
                df1['Fail'] = fclass
                df1['% of Pass'] = pass_percentage
                df1['% of Fail'] = fail_percentage

                st.write(df1)

                if st.checkbox("Do you Want to Download Excel File"):
                    sheet_name = st.text_input("Enter Sheet Name")
                    if sheet_name is not None:
                        df.index = np.arange(1, len(df) + 1)
                        df.to_excel("SE First Semester.xlsx", sheet_name=sheet_name)

                return df











    if choice == 'EDA':
        st.subheader("Exploratory Data Analysis")
        #data = st.file_uploader("Upload a Dataset", type=["pdf"])

        if st.checkbox("S.E First Semester"):
            data1 = st.file_uploader("Upload a Dataset", type=["pdf"])
            if data1 is not None:
                df1=SE1sem(data1)

        if st.checkbox("T.E First Semester"):
            data1 = st.file_uploader("Upload a Dataset", type=["pdf"])
            if data1 is not None:
                df1=TE1sem(data1)

        if st.checkbox("B.E First Semester"):
            data1 = st.file_uploader("Upload a Dataset", type=["pdf"])
            if data1 is not None:
                df1=BE1sem(data1)
        

        Class_wise=st.file_uploader('Please Upload seat no Class Wise',type=["xlsx"])
        st.write(Class_wise)

        if st.checkbox("Show Shape"):
            st.write(df1.shape)

        if st.checkbox("Show Columns"):
            all_columns = df1.columns.to_list()
            st.write(all_columns)

        if st.checkbox("Summary"):
            st.write(df1.describe())
            # st.write(df1.count())
            # st.write(df1.mean())
            # st.write(df1.max())
            # st.write(df1.min())

        if st.checkbox("Show Selected Columns"):
            all_columns = df1.columns.to_list()
            selected_columns = st.multiselect("Select Columns", all_columns)
            new_df = df1[selected_columns]
            st.dataframe(new_df)



        if st.checkbox("Show Value Counts"):
            st.write(df1.iloc[:, -1].value_counts())
            fig, ax = plt.subplots(figsize=(26,10))
            plt.xticks(size=13)
            plt.yticks(size=13)

            ax=sns.countplot(data=df1,x='SGPA')
            for p in ax.patches:
                ax.annotate(f'\n{p.get_height()}', (p.get_x() + 0.2, p.get_height()), color='black', size=15,
                            ha="center")
            st.pyplot()

        # if st.checkbox("Correlation Plot(Matplotlib)"):
        #     plt.matshow(df1.corr())
        #     st.pyplot()

        if st.checkbox("Correlation Plot(Seaborn)"):
            st.write(sns.heatmap(df1.corr(), annot=True))
            st.pyplot()

        if st.checkbox("Pie Plot"):
            all_columns = df1.columns.to_list()
            column_to_plot = st.selectbox("Select 1 Column", all_columns)
            pie_plot = df1[column_to_plot].value_counts().plot.pie(autopct="%1.1f%%")
            st.write(pie_plot)
            st.pyplot()



    elif choice == 'Plots':
        st.subheader("Data Visualization")
        data = st.file_uploader("Upload a Dataset", type=["pdf"])
        if data is not None:
            if st.checkbox("S.E First Semester"):
                df1 = SE1sem(data)

            if st.checkbox("T.E First Semester"):
                df1 = TE1sem(data)

            if st.checkbox("B.E First Semester"):
                df1 = BE1sem(data)



            if st.checkbox("Show Value Counts"):
                st.write(df1.iloc[:, -1].value_counts().plot(kind='bar'))
                st.pyplot()

            # Customizable Plot

            all_columns_names = df1.columns.tolist()
            type_of_plot = st.selectbox("Select Type of Plot", ["area", "bar", "line", "hist", "box", "kde"])
            selected_columns_names = st.multiselect("Select Columns To Plot", all_columns_names)

            if st.button("Generate Plot"):
                st.success("Generating Customizable Plot of {} for {}".format(type_of_plot, selected_columns_names))

                # Plot By Streamlit
                if type_of_plot == 'area':
                    cust_data = df1[selected_columns_names]
                    st.area_chart(cust_data)

                elif type_of_plot == 'bar':
                    cust_data = df1[selected_columns_names]
                    st.bar_chart(cust_data)

                elif type_of_plot == 'line':
                    cust_data = df1[selected_columns_names]
                    st.line_chart(cust_data)

                # Custom Plot
                elif type_of_plot:
                    cust_plot = df1[selected_columns_names].plot(kind=type_of_plot)
                    st.write(cust_plot)
                    st.pyplot()


if __name__ == '__main__':
    main()