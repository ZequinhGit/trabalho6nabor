package com.github.JoaoPem.computacaodistribuida.config;

import org.springframework.boot.web.servlet.ServletRegistrationBean;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.ClassPathResource;
import org.springframework.ws.config.annotation.EnableWs;
import org.springframework.ws.transport.http.MessageDispatcherServlet;
import org.springframework.ws.wsdl.wsdl11.DefaultWsdl11Definition;
import org.springframework.xml.xsd.SimpleXsdSchema;
import org.springframework.xml.xsd.XsdSchema;

@EnableWs
@Configuration
public class WebServiceConfig {

    @Bean
    public ServletRegistrationBean<MessageDispatcherServlet> messageDispatcherServlet(ApplicationContext context) {
        MessageDispatcherServlet servlet = new MessageDispatcherServlet();
        servlet.setApplicationContext(context);
        servlet.setTransformWsdlLocations(true);
        return new ServletRegistrationBean<>(servlet, "/soap/*");
    }

    @Bean(name = "users")
    public DefaultWsdl11Definition userAccountWsdlDefinition(XsdSchema userAccountSchema) {
        DefaultWsdl11Definition wsdl = new DefaultWsdl11Definition();
        wsdl.setPortTypeName("UserAccountPort");
        wsdl.setLocationUri("/soap");
        wsdl.setTargetNamespace("http://example.com/users/soap");
        wsdl.setSchema(userAccountSchema);
        return wsdl;
    }

    @Bean
    public XsdSchema userAccountSchema() {
        return new SimpleXsdSchema(new ClassPathResource("xsd/user-account.xsd"));
    }

    @Bean(name = "music")
    public DefaultWsdl11Definition musicWsdlDefinition(XsdSchema musicSchema) {
        DefaultWsdl11Definition wsdl = new DefaultWsdl11Definition();
        wsdl.setPortTypeName("MusicPort");
        wsdl.setLocationUri("/soap");
        wsdl.setTargetNamespace("http://example.com/music/soap");
        wsdl.setSchema(musicSchema);
        return wsdl;
    }

    @Bean
    public XsdSchema musicSchema() {
        return new SimpleXsdSchema(new ClassPathResource("xsd/music.xsd"));
    }

    @Bean(name = "playlist")
    public DefaultWsdl11Definition playlistWsdlDefinition(XsdSchema playlistSchema) {
        DefaultWsdl11Definition wsdl = new DefaultWsdl11Definition();
        wsdl.setPortTypeName("PlaylistPort");
        wsdl.setLocationUri("/soap");
        wsdl.setTargetNamespace("http://example.com/playlists/soap");
        wsdl.setSchema(playlistSchema);
        return wsdl;
    }

    @Bean
    public XsdSchema playlistSchema() {
        return new SimpleXsdSchema(new ClassPathResource("xsd/playlist.xsd"));
    }

}
