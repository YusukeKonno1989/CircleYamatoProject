function footer(rootDir){
    $.ajax({
        url: rootDir + "footer.html", // 読み込むHTMLファイル
        cache: false,
        async: false,
        dataType: 'html',
        success: function(html){
            html = html.replace(/\{\$root\}/g, rootDir);
            document.write(html);
        }
    });
}