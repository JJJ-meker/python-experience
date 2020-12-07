# 豆瓣网页分析

```mermaid
graph LR
A[https://movie.douban.com]--request1-->B[a标签]
B --获得--> C[电影连接地址href]
B --> D[电影名] --> J[存储]
B --> G[海报链接src]
C --request2--> E[电影详情页]
E --分析--> F[演员] --> J
G --requets2--> H[海报图片] --> M[存储jpg文件]
E --分析--> I[预告片地址href]
I --request3--> K[预告片播放界面网址href]
K --request4--> L[预告片内容] --> N[存储mp4文件]
```