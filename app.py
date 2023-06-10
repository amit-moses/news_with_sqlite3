from flask import Flask, render_template, request,redirect
import sqlite3

# init database 

con = sqlite3.connect("news.db", check_same_thread=False)
cur = con.cursor()
all_cat = cur.execute("SELECT * FROM categorey").fetchall()
all_cat_set = {item[1]: item[0] for item in all_cat}
all_cat_set2 = {item[0]: item[1] for item in all_cat}
# starting flask app
app = Flask(__name__)

@app.route("/")
@app.route("/<pg>")
def news(pg = ''):
   if pg in all_cat_set:
      res = cur.execute(f"SELECT rowid,* FROM article WHERE cat='{all_cat_set[pg]}'")
   else:
      res = cur.execute(f"SELECT rowid,* FROM article")
   articles = res.fetchall()
   return render_template("article.html", news=articles, cat=all_cat)



@app.route("/delete/<id>", methods=["GET","POST"])
def delete(id):
   goto=''
   res = cur.execute(f"SELECT * FROM article WHERE rowid={id}").fetchall()
   if len(res)>0:
      goto = res[0][3]
      cur.execute(f"DELETE FROM article WHERE rowid={id}")
      con.commit()
   return redirect(f'/{all_cat_set2[goto]}')


@app.route("/add_article", methods=["GET","POST"])
@app.route("/article/<id>", methods=["GET","POST"])
def add_article(id = 0):
   if request.method == "POST":
      title = request.form.get("title")
      content = request.form.get("content")
      image_url = request.form.get("image-url")
      category = request.form.get("category")
      if id == "0":
         print('balagan')
         cur.execute(f"INSERT INTO article VALUES ('{title}', '{content}', '{image_url}','{category}')")
      else: 
         res = cur.execute(f"""UPDATE article SET title = '{title}', content = '{content}', 
        image='{image_url}',cat='{category}' WHERE rowid={id};""")
      con.commit()
      return redirect(f'/{all_cat_set2[category]}')
   else:
      items_list = (''),(''),(''),(''),('0')
      if id != 0:
         res = cur.execute(f"SELECT *,rowid FROM article WHERE rowid={id}").fetchall()
         if len(res) > 0:
            items_list = res[0]
      print (items_list, 'bdika')
      return render_template("add_article.html", cat=all_cat, values=items_list)


   


if __name__ == '__main__':
   app.run(debug=True, port=9000)