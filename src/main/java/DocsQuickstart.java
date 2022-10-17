import com.google.api.client.auth.oauth2.Credential;
import com.google.api.client.extensions.java6.auth.oauth2.AuthorizationCodeInstalledApp;
import com.google.api.client.extensions.jetty.auth.oauth2.LocalServerReceiver;
import com.google.api.client.googleapis.auth.oauth2.GoogleAuthorizationCodeFlow;
import com.google.api.client.googleapis.auth.oauth2.GoogleClientSecrets;
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.http.javanet.NetHttpTransport;
import com.google.api.client.json.JsonFactory;
import com.google.api.client.util.store.FileDataStoreFactory;
import com.google.api.services.docs.v1.Docs;
import com.google.api.services.docs.v1.DocsScopes;
import com.google.api.services.docs.v1.model.*;
import com.google.api.client.json.gson.GsonFactory;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.security.GeneralSecurityException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class DocsQuickstart {
    private static final String APPLICATION_NAME = "Google Docs API Java Quickstart";
    private static final JsonFactory JSON_FACTORY = GsonFactory.getDefaultInstance();
    private static final String TOKENS_DIRECTORY_PATH = "tokens";
    private static final String DOCUMENT_ID = "161eG6oAB1G_YMum66AeZzbiRpCwaq5Ic8pF7kSyK-Z8";
    private static final List<String> SCOPES = Collections.singletonList(DocsScopes.DOCUMENTS);
    private static final String CREDENTIALS_FILE_PATH = "/credentials.json";
    /**
     * Creates an authorized Credential object.
     *
     * @param HTTP_TRANSPORT The network HTTP Transport.
     * @return An authorized Credential object.
     * @throws IOException If the credentials.json file cannot be found.
     */
    private static Credential getCredentials(final NetHttpTransport HTTP_TRANSPORT) throws IOException {
        // Load client secrets.
        InputStream in = DocsQuickstart.class.getResourceAsStream(CREDENTIALS_FILE_PATH);
        GoogleClientSecrets clientSecrets = GoogleClientSecrets.load(JSON_FACTORY, new InputStreamReader(in));

        // Build flow and trigger user authorization request.
        GoogleAuthorizationCodeFlow flow = new GoogleAuthorizationCodeFlow.Builder(
                HTTP_TRANSPORT, JSON_FACTORY, clientSecrets, SCOPES)
                .setDataStoreFactory(new FileDataStoreFactory(new java.io.File(TOKENS_DIRECTORY_PATH)))
                .setAccessType("offline")
                .build();
        LocalServerReceiver receier = new LocalServerReceiver.Builder().setPort(8888).build();
        return new AuthorizationCodeInstalledApp(flow, receier).authorize("user");
    }

    public static void main(String... args) throws IOException, GeneralSecurityException {
        // Build a new authorized API client service.
        final NetHttpTransport HTTP_TRANSPORT = GoogleNetHttpTransport.newTrustedTransport();
        Docs service = new Docs.Builder(HTTP_TRANSPORT, JSON_FACTORY, getCredentials(HTTP_TRANSPORT))
                .setApplicationName(APPLICATION_NAME)
                .build();

        Document response = service.documents().get(DOCUMENT_ID).execute();
        String title = response.getTitle();
        System.out.printf("The title of the doc is: %s\n", title);

        List<Request> requests = new ArrayList<>();

        // Format text
        requests.add(new Request().setUpdateParagraphStyle(new UpdateParagraphStyleRequest()
                .setRange(new Range()
                        .setStartIndex(1)
                        .setEndIndex(10))
                .setParagraphStyle(new ParagraphStyle()
                        .setNamedStyleType("HEADING_1")
                        .setSpaceAbove(new Dimension()
                                .setMagnitude(10.0)
                                .setUnit("PT"))
                        .setSpaceBelow(new Dimension()
                                .setMagnitude(10.0)
                                .setUnit("PT")))
                .setFields("namedStyleType,spaceAbove,spaceBelow")
        ));

        // Add text
        String intro  = "Here is the link to your video clip: ";
        String link = "https://www.youtube.com\n";
        requests.add(new Request().setInsertText(new InsertTextRequest()
                .setText(intro + link)
                .setLocation(new Location().setIndex(1))));

        // format link
        requests.add(new Request()
                .setUpdateTextStyle(new UpdateTextStyleRequest()
                        .setRange(new Range()
                                .setStartIndex(intro.length()+1)
                                .setEndIndex(intro.length()+link.length()))
                        .setTextStyle(new TextStyle()
                                .setLink(new Link()
                                        .setUrl(link)))
                        .setFields("link")));


        BatchUpdateDocumentRequest body = new BatchUpdateDocumentRequest().setRequests(requests);
        BatchUpdateDocumentResponse responseFormatText = service.documents()
                .batchUpdate(DOCUMENT_ID, body).execute();
//        System.out.println(responseFormatText);

    }
}
