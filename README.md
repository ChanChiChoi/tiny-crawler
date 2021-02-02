# tiny-crawler   

- csdn: you can login in www.csdn.com  by this script    
- libgen: you can replace the keyword to search the books and papers from libgen.io. the code of libgen.py is so short, so i do not format the code     
- arxiv_search_pdfDownload: you can just replace the keyword to search papers from arxiv.org, the download links and paper filename will save in the correspond txt file       
- arxiv_0704-now_wAbstract: get the paper meta info by month from 2007.04 to now    
- arxiv_9108-0703_wAbstract.py: get the paper meta info from 1991.08 to 2007.03   
ps:**because arxiv change it's url rule from 2007.03, so we need two different script to scrapy the data**.
- arxiv_byArchive_woAbstract: download the paper meta info in bulk by access [arxiv archive](https://arxiv.org/archive). but it can get the papers' abstract

## paperMeta4arxiv
because the arxiv do not support Regular search, so i scrapy the paper meta info here     
the format as follow:     
```
              <id> \t <paper name> \t <subject> \t <authors>   
```
you can find the paper meta info from 2008.01 to 2018.04


## A better way to get books from libgen.io
1) download the [libgen_content.rar](http://libgen.io/libgen/content/libgen_content.rar). After decompression, you'll get the libgen_content.csv, that contains the whole 2319076 digit books info;  
```
'id', 'title', 'volumeinfo', 'series', 'periodical', 'author', 'year', 'edition', 'publisher', 'city', 'pages', 'language', 'topic', 'library', 'issue', 'identifier', 'issn', 'asin', 'udc', 'lbc', 'ddc', 'lcc', 'doi',  'googlebookid', 'openLibraryid', 'commentary', 'dpi', 'color', 'cleaned', 'orientation', 'paginated', 'scanned', 'bookmarked', 'searchable', 'filesize', 'extension', 'md5', 'generic', 'visible', 'locator', 'local', 'timeadded', 'timelastmodified', 'coverurl','identifierwodash', 'tags', 'pagesinfile'
```
2) you should delete some confusing string:  
```
sed 's/\\"/ /g' libgen_content.csv > libgen_content1.csv
# sed -i '/"ban"/d;/"del"/d;/"Russian"/d' libgen_content1.csv # should not run this
```
3) use grep command to filter the lines you selected;    
```
grep -i mathematics libgen_content1.csv > result.csv
```
4) then, use "libgen_createDownloadlink.py" to create "libgen.io.{keyword}.txt", each line in the txt files contain raw book info and different mirror downloadlinks! 
```
python libgen_createDownloadlink.py result.csv 
```
5） because of the libgen.pw website changes download link frequently, we also need another script to update the libgen.pw downloadlink in "result.csv"
```
python libgen_updateLibgenPWLink.py -f result.csv -n 20
```

ps:
```
awk -F'\t' '{print "- " $4 " .["$2"](https://arxiv.org/pdf/"$1") [J]. arXiv preprint arXiv:"$1"."}' file.txt >file1.txt
```
