using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using System.Drawing.Imaging;
using System.Text.RegularExpressions;
using System.Drawing.Drawing2D;
using System.Diagnostics;

namespace AppRecomender
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        private void positionApps(GroupBox g, StreamReader sr, int n)
        {
            for (int i = 0; i < n; i++)
            {
                string icon = sr.ReadLine().Split(' ')[0].ToString();
                PictureBox p = new PictureBox();
                p.Size = new Size(30, 30);
                p.Left = g.Left + 20;
                p.Top = g.Top + 20 + i * (p.Height + 10);
                p.Visible = true;
                Controls.Add(p);
                p.BringToFront();
                g.SendToBack();
                p.Load(icon);
                p.SizeMode = PictureBoxSizeMode.StretchImage;
            }
        }
        private void button1_Click(object sender, EventArgs e)
        {
            int user = int.Parse(textBox1.Text);
           
            run_cmd(user);

            StreamReader srPearson = new StreamReader("pearson_file");
            StreamReader srCosine = new StreamReader("cosine_file");
            StreamReader srMinkowski = new StreamReader("minkowski_file");
            StreamReader srManhattan = new StreamReader("manhattan_file");

            positionApps(groupBox1, srPearson, 5);
            positionApps(groupBox2, srManhattan, 5);
            positionApps(groupBox3, srMinkowski, 5);
            positionApps(groupBox4, srCosine, 5);



        }
        private void run_cmd(int user)
        {
            // full path of python interpreter
            string python = @"C:/Python34/python.exe";

            // python app to call
            string myPythonApp = "app_recommender.py";

            // dummy parameters to send Python script

            // Create new process start info
            ProcessStartInfo myProcessStartInfo = new ProcessStartInfo(python);

            // make sure we can read the output from stdout
            myProcessStartInfo.UseShellExecute = false;
            myProcessStartInfo.RedirectStandardOutput = true;

            // start python app with 2 arguments 
            // 1st arguments is pointer to itself, 2nd is actual argument we want to send
            myProcessStartInfo.Arguments = myPythonApp + " " + user;

            Process myProcess = new Process();
            // assign start information to the process
            myProcess.StartInfo = myProcessStartInfo;

            Text = string.Format("Calling Python script with arguments {0}", user);
            // start the process
            myProcess.Start();

            // Read the standard output of the app we called. 
            // in order to avoid deadlock we will read output first and then wait for process terminate:
            StreamReader myStreamReader = myProcess.StandardOutput;
            string myString = myStreamReader.ReadLine();

            /*if you need to read multiple lines, you might use:
                string myString = myStreamReader.ReadToEnd() */

            // wait exit signal from the app we called and then close it.
            myProcess.WaitForExit();
            myProcess.Close();

            // write the output we got from python app
            Text = "Value received from script: " + myString;
           
        }
    }
}
