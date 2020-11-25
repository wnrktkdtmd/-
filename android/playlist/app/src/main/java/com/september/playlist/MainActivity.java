package com.september.playlist;

import android.content.ContentValues;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.SearchView;

import androidx.appcompat.app.AppCompatActivity;

import java.util.ArrayList;


public class MainActivity extends AppCompatActivity {
    SearchView searchView;
    // 빈 데이터 리스트 생성.
    ArrayList<String> items;
    ArrayAdapter adapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) { //onCreateOptionsMenu는 자동 호출됨
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        items = new ArrayList<String>() ;
        // ArrayAdapter 생성. 아이템 View를 선택(single choice)가능하도록 만듦.
        adapter = new ArrayAdapter(this, android.R.layout.simple_list_item_1, items) ;

        // listview 생성 및 adapter 지정.
        final ListView listview = (ListView) findViewById(R.id.listview1) ;
        listview.setAdapter(adapter) ;


    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.menu_main, menu);

        MenuItem menuItem = menu.findItem(R.id.menu_main_search);
        searchView = (SearchView) menuItem.getActionView();
        searchView.setQueryHint("단어나 문장 입력");
        searchView.setOnQueryTextListener(queryTextListener);

        return super.onCreateOptionsMenu(menu);
    }

    private SearchView.OnQueryTextListener queryTextListener = new SearchView.OnQueryTextListener() {
        @Override
        public boolean onQueryTextSubmit(String query) {
            // 텍스트 입력 후 검색 버튼이 눌렸을 때의 이벤트

            // URL 설정.
            String url = "https://september-n2yuvn4wna-de.a.run.app?label=";
            url += query;
            url += "&num=";
            url += Integer.toString(10);
            url += "&sentence=";
            url += Integer.toString(0);

            // AsyncTask를 통해 HttpURLConnection 수행.
            ContentValues val = new ContentValues();

            NetworkTask networkTask = new NetworkTask(url);
            networkTask.execute();
            return false;
        }

        @Override
        public boolean onQueryTextChange(String newText) {
            // 검색 글 한자 한자 눌렸을 때의 이벤트
            return false;
        }

        class NetworkTask extends AsyncTask<Void, Void, String> {

            private String url;

            public NetworkTask(String url) {
                this.url = url;
            }

            @Override
            protected String doInBackground(Void... params) {

                String result; // 요청 결과를 저장할 변수.
                RequestHttpURL requestHttpURLConnection = new RequestHttpURL();
                result = requestHttpURLConnection.request(url); // 해당 URL로 부터 결과물을 얻어온다.

                return result;
            }

            @Override
            protected void onPostExecute(String s) {
                super.onPostExecute(s);
                s = s.substring(1,s.length()-2);
                //doInBackground()로 부터 리턴된 값이 onPostExecute()의 매개변수로 넘어오므로 s를 출력한다.
                String[] arr = s.split("@");
                for (int i = 0; i < arr.length; i++) {
                    items.add(arr[i]);
                }

                adapter.notifyDataSetChanged();
            }
        }
    };

}