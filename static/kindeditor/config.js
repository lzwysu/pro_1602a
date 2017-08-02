/**
 * Created by Alice on 2016/5/30.
 */
KindEditor.ready(function(K) {
        K.create('#id_content',{
            width : '800px',
            height : '300px',
            uploadJson: '/admin/upload/kindeditor',
        });
});