# Topic Model Tool

主要用来对一系列的文章进行话题提取。

### 主要特征
* 支持对一定时间段内的文章进行话题提取。
* 支持不同数据来源的话题提取。
* 对包含某关键字的文档进行话题提取。
* 支持动态本地字典构造

### 使用方式
主要通过运行`topic.py`脚本来进行特征提取。

    usage: topic.py [-h] [-d DAYS] [-s [SOURCE [SOURCE ...]]]
                    [-k [KEYS [KEYS ...]]]
    
    extract topic from specific documents
    
    optional arguments:
      -h, --help            show this help message and exit
      -d DAYS, --days DAYS  how many days of documents before today you want to
                            analyse
      -s [SOURCE [SOURCE ...]], --source [SOURCE [SOURCE ...]]
                            The source of the doucments, could be blog, news,
                            magazines, support multi sources
      -k [KEYS [KEYS ...]], --keys [KEYS [KEYS ...]]
                            The keywords you want the documents contain, support
                            multisources
    

提取十天之内有关平安银行的话题，数据来源为news: `python topic.py -d 10 -s news -k 平安银行`。

日志样例：

    2014-08-16 19:54:42,216 : INFO : command line:Namespace(days=10, keys=['平安银行'], source=['news'])
    2014-08-16 19:54:42,217 : INFO : start:datetime.datetime(2014, 8, 6, 19, 54, 42, 216741)
    2014-08-16 19:54:42,217 : INFO : end:datetime.datetime(2014, 8, 16, 19, 54, 42, 216741)
    2014-08-16 19:55:26,878 : INFO : There are 156 documents
    2014-08-16 19:55:26,878 : INFO : Building the dictionary...
    2014-08-16 19:55:28,998 : INFO : built Dictionary(281970 unique tokens: ['边检', '探归', '解开', '鲁波', '憬']...) from 0 documents (total 0 corpus positions)
    2014-08-16 19:55:28,998 : INFO : saving dictionary mapping to ./dict.txt
    2014-08-16 19:55:30,497 : INFO : There are 281970 unique words in dictionary
    2014-08-16 19:57:03,422 : INFO : number of corpus 156
    2014-08-16 19:57:03,422 : INFO : Construction Completed.
    2014-08-16 19:57:03,422 : INFO : Building the tfidf model...
    2014-08-16 19:57:03,422 : INFO : collecting document frequencies
    2014-08-16 19:57:03,422 : INFO : PROGRESS: processing document #0
    2014-08-16 19:57:03,435 : INFO : calculating IDF weights for 156 documents and 281951 features (45276 matrix non-zeros)
    2014-08-16 19:57:03,445 : INFO : Construction Completed.
    2014-08-16 19:57:03,445 : INFO : Building the LSI model...
    2014-08-16 19:57:03,445 : INFO : Topic number is 12
    2014-08-16 19:57:03,484 : INFO : using serial LSI version on this node
    2014-08-16 19:57:03,484 : INFO : updating model with new documents
    2014-08-16 19:57:03,555 : INFO : preparing a new chunk of documents
    2014-08-16 19:57:03,555 : DEBUG : converting corpus to csc format
    2014-08-16 19:57:03,570 : INFO : using 100 extra samples and 2 power iterations
    2014-08-16 19:57:03,571 : INFO : 1st phase: constructing (281970, 112) action matrix
    2014-08-16 19:57:03,633 : INFO : orthonormalizing (281970, 112) action matrix
    2014-08-16 19:57:04,005 : DEBUG : computing QR of (281970, 112) dense matrix
    2014-08-16 19:57:08,974 : DEBUG : running 2 power iterations
    2014-08-16 19:57:09,779 : DEBUG : computing QR of (281970, 112) dense matrix
    2014-08-16 19:57:14,162 : DEBUG : computing QR of (281970, 112) dense matrix
    2014-08-16 19:57:18,218 : INFO : 2nd phase: running dense svd on (112, 156) matrix
    2014-08-16 19:57:18,688 : INFO : computing the final decomposition
    2014-08-16 19:57:18,688 : INFO : keeping 12 factors (discarding 62.555% of energy spectrum)
    2014-08-16 19:57:18,748 : INFO : processed documents up to #156
    2014-08-16 19:57:18,895 : INFO : topic #0(3.099): -0.397*"电商" + -0.183*"平台" + -0.162*"分钟" + -0.151*"网站" + -0.151*"理财产品" + -0.125*"系" + -0.119*"P2P" + -0.111*"支付" + -0.109*"银行" + -0.107*"发行"
    2014-08-16 19:57:18,913 : INFO : topic #1(2.661): 0.414*"电商" + -0.205*"发行" + 0.180*"分钟" + 0.177*"网站" + -0.167*"存单" + -0.132*"理财产品" + -0.119*"挂钩" + -0.115*"美元" + 0.115*"平台" + -0.114*"收益率"
    2014-08-16 19:57:18,930 : INFO : topic #2(2.343): 0.428*"存单" + 0.315*"发行" + 0.270*"同业" + -0.224*"支付" + -0.200*"P2P" + 0.178*"亿元" + 0.135*"电商" + -0.131*"收单" + -0.127*"违规" + -0.122*"商户"
    2014-08-16 19:57:18,948 : INFO : topic #3(2.254): -0.289*"美元" + -0.270*"理财产品" + 0.266*"存单" + -0.206*"挂钩" + 0.185*"支付" + -0.165*"收益率" + 0.164*"同业" + 0.159*"P2P" + -0.142*"指数" + -0.136*"结构性"
    2014-08-16 19:57:18,965 : INFO : topic #4(2.165): -0.496*"股" + 0.164*"理财产品" + -0.159*"五家" + 0.143*"美元" + -0.129*"板块" + 0.119*"存单" + -0.118*"点" + -0.113*"成份股" + -0.110*"流出" + 0.106*"挂钩"
    2014-08-16 19:57:18,969 : INFO : Construction Complete.
    2014-08-16 19:57:23,935 : INFO : have saved the topics into the database
    2014-08-16 19:57:23,976 : INFO : function test has spend 161.75974011421204 seconds

运行之后脚本会自动把提取出来的话题放入到topics collection中。以便之后被用来进行可视化。
