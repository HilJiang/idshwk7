clear ;
clc;
      
%-----------------------读入图像-------------------------------------%
markbefore=imread('p203.bmp');
markbefore2=rgb2gray(markbefore);
mark=im2bw(markbefore2);    
figure(1);      
subplot(2,3,1);   
imshow(mark),title('水印图像');  
[rm,cm]=size(mark);  
cover=imread('pic.bmp');
cover1=imresize(cover,[512,512]);
cover_image=rgb2gray(cover1);
subplot(2,3,2),imshow(cover_image,[]),title('原始图像'); 
 
before=blkproc(cover_image,[8 8],'dct2');   %将载体图像的灰度层分为8×8的小块，每一块内做二维DCT变换，结果记入矩阵before
I=mark;
alpha=50;     %尺度因子,控制水印添加的强度,决定了频域系数被修改的幅度
k1=randn(1,8);  %产生两个不同的随机序列
k2=randn(1,8);
after=before;   %初始化载入水印的结果矩阵
for i=1:rm          %在中频段嵌入水印
    for j=1:cm
        x=(i-1)*8;
        y=(j-1)*8;
        if mark(i,j)==1
            k=k1;
        else
            k=k2;
        end;
        after(x+1,y+8)=before(x+1,y+8)+alpha*k(1);
        after(x+2,y+7)=before(x+2,y+7)+alpha*k(2);
        after(x+3,y+6)=before(x+3,y+6)+alpha*k(3);
        after(x+4,y+5)=before(x+4,y+5)+alpha*k(4);
        after(x+5,y+4)=before(x+5,y+4)+alpha*k(5);
        after(x+6,y+3)=before(x+6,y+3)+alpha*k(6);
        after(x+7,y+2)=before(x+7,y+2)+alpha*k(7);
        after(x+8,y+1)=before(x+8,y+1)+alpha*k(8);
    end;
end;
result=blkproc(after,[8 8],'idct2');    %将经处理的图像分为8×8的小块，每一块内做二维DCT逆变换
result = uint8(result);
imwrite(result,'watermarked.bmp','bmp');     %隐写图像命名为watermarked.bmp
subplot(2,3,3),imshow(result,[]),title('隐写图像');   


        subplot(2,3,4);
        imshow(result,[]);
        title('水印图像');
        withmark=result;
        subplot(2,3,4);
        imshow(result,[]);
        title('图像');
        withmark=result;

 
%------------------------水印提取-----------------------------%
%
after_2=blkproc(withmark,[8,8],'dct2');   %此步开始提取水印，将灰度层分块进行DCT变换
p=zeros(1,8);        %初始化提取数值用的矩阵
mark_2 = zeros(rm,cm);
for i=1:rm
    for j=1:cm
        x=(i-1)*8;y=(j-1)*8;
        p(1)=after_2(x+1,y+8);         %将之前改变过数值的点的数值提取出来
        p(2)=after_2(x+2,y+7);
        p(3)=after_2(x+3,y+6);
        p(4)=after_2(x+4,y+5);
        p(5)=after_2(x+5,y+4);
        p(6)=after_2(x+6,y+3);
        p(7)=after_2(x+7,y+2);
        p(8)=after_2(x+8,y+1);
        if corr2(p,k1)>corr2(p,k2)  %corr2计算两个矩阵的相似度，越接近1相似度越大
            mark_2(i,j)=1;              %比较提取出来的数值与随机频率k1和k2的相似度，还原水印图样
        else
            mark_2(i,j)=0;
        end
    end
end
subplot(2,3,5);
mark_2 = uint8(mark_2);
imshow(mark_2,[]),title('提取水印');
subplot(2,3,6);
imshow(mark),title('原水印图像');

