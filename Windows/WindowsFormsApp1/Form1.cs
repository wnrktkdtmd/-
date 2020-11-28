using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.IO;
using System.Windows.Forms;

namespace WindowsFormsApp1
{
    public partial class Form1 : Form
    {

        public Form1()
        {

            InitializeComponent();


        }

        private void Button1_Click(object sender, System.EventArgs e)
        {

            int title_or_sentense = -1;
            if (radioButton1.Checked == true) { title_or_sentense = 0; }
            else if (radioButton2.Checked == true) { title_or_sentense = 1; }
            
            string url = "https://september-n2yuvn4wna-de.a.run.app/?label=";
            url += textBox1.Text;
            url += "&num=";
            url += numericUpDown1.Value.ToString();
            url += "&sentence=";
            url += title_or_sentense.ToString();

            string responseText = string.Empty;

            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);
            request.Method = "GET";
            request.Timeout = 30 * 1000; // 30초

            using (HttpWebResponse resp = (HttpWebResponse)request.GetResponse())
            {
                HttpStatusCode status = resp.StatusCode;
                Console.WriteLine(status);  // 정상이면 "OK"

                Stream respStream = resp.GetResponseStream();
                using (StreamReader sr = new StreamReader(respStream))
                {
                    responseText = sr.ReadToEnd();
                }
            }

            responseText = responseText.Substring(1, responseText.Length - 2);
            String ret = "";
            String[] arr = responseText.Split('@');
            for (int i = 0; i < arr.Length; i++)
            {
                ret += arr[i];
                ret += "\r\n";
            }

            textBox2.Text = ret;

        }

        private void textBox1_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Enter)
            {
                Button1_Click(sender, e);
            }

        }

    }
}
