通过指定关键字爬取知乎所有问题

使用环境:python3.6
使用模块:requests
---
	思路: 
	1.查看网页结构发现回答使用的是异步加载,所以直接找的数据接口保存json文件
	2.接口是20条数据一个接口,想了很久能不能拼接接口url一次性返回所有数据,结果失败了...
	3.没有找到所有数据的接口就根据接口规律循环获取数据

---
	遇到的问题:
	1.问题详情页的url不能直接从接口获取,需要切割在拼接才能获取
	'''
	url = data.get('object').get('url').replace('api', 'www').rsplit('/', 2)   # ['https://www.zhihu.com', 'answers', '424927405']
    q_type = data.get('object').get('question').get('type')
    q_id = data.get('object').get('question').get('id')
    full_url = url[0] + '/' + q_type + '/' + q_id + '/' + url[1].replace('answers', 'answer') + '/' + url[2]
    print(full_url)
	'''
	2.把MongoDB数据库中的数据导出为excel表

---
	收获:
		学会了把MongoDB数据库中的数据导出为excel表
	导出语句:
	'''
	mongoexport -d zhihu -c questions -f _id,search_terms,search_rank,question_url,question_title,question_follow_num,question_view_num,question_top_answer_username,question_top_answer_id  --csv -o C:\Users\Administrator\Desktop\zhihu.csv
	'''
