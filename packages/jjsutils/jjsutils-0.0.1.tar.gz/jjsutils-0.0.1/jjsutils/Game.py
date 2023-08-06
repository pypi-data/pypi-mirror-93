class Game():
    title = '' 
    
    def __init__(self, tag):
        self.title = self.get_text(tag, 'div.WsMG1c.nnK0zc')
        self.comp = self.get_text(tag, 'div.KoLSrc')
        self.price = self.get_text(tag, 'span.VfPpfd.ZdBevf.i5DZme')
        
        # 복잡한 생성자코드는 뒤로 밀기. 나중에는 함수로 빼야한다.
        self.rating = self.get_rating(tag, 'div.vQHuPe.bUWb7c.D3FNOd', 'style')

    # 생성자에 있던 복잡한 코드는 인스턴스메소드로 정리한다.
    def get_rating(self, parent_tag, selector, attr):
        cr = self.get_attr(parent_tag, selector, attr)
        percent_strs = cr.split(" ")
        if len(percent_strs) < 2:  # 0or1
            return 0.0
        else:
            return float(percent_strs[1].replace("%", ""))
            
    def get_tag(self, parent_tag, selector):
        tag = parent_tag.select(selector) 
        if tag == None or len(tag) == 0 :
            return None
        else:
            return tag[0] 
                
    def get_text(self, parent_tag, selector):
        tag = self.get_tag(parent_tag, selector)
        return tag.text.strip()
        
    def get_attr(self, parent_tag, selector, attr_name):
        tag = self.get_tag(parent_tag, selector)
        attr = tag.get(attr_name)
        return "" if  attr == None else attr.strip()
    
    # 오버라이딩은, default로 정의된 부모것의 __str__을 덮어쓰는 것. 이제껏 하던것
    # 오버로드는 __str__함수에 새롭게 정의한 함수를 호출하도록 하는 것
    # print(인스턴스)로 __str__이 호출되면, 새롭게 정의한 함수 to_str을 호출하여 값을 반환받아 return되서 print
    #                             밖에서 인스턴스.to_str()을 호출하면, 값을 반환
    #    __str__는 어차피 값을 반환시키는 것을 print하므로, 값을 반환하는 함수를 정의할 때, 그놈을 호출시키도록 한다.
    #   1) str값 반환함수가 있어야, file.write를 시킴
    #   2) str값 반환함수가 있으면, __str__에서 str값 반환을 한번더 할 필요없이 1)에서 정의한 것을 호출해서 return받기
    #   3) 오버로드는 어차피 다른함수가 똑같은 짓을 하고 있다면, 파이썬내장함수 __str__에서 호출되도록 함.
    def __str__(self):
        #return f"{self.title}\t{self.comp}\t{self.price}\t{self.rating:.1f}" # 소수점은 너무 길면 안되니까,  :.1f 를 적어준다.
        return self.to_str()
        
    def to_str(self):
        return f"{self.title}\t{self.comp}\t{self.price}\t{self.rating:.1f}" # 소수점은 너무 길면 안되니까,  :.1f 를 적어준다.